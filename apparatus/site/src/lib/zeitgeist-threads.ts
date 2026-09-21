/**
 * Thread registry for zeitgeist items: schema, validation and resolution. Pure.
 *
 * An item's title is a sentence written fresh each week, so its slug never
 * recurs: across the first 35 readings, 402 of 426 item ids were singletons.
 * A thread is the named thing those sentences are about ("iran-war"). The
 * registry maps item slugs to threads explicitly, and it is committed and
 * reviewed like any other text.
 *
 * Decisions, not accidents — do not undo:
 * - Resolution is exact. The matcher this replaces also captured any title that
 *   merely *contained* a variant's words, silently. A slug is in a thread
 *   because someone put it there.
 * - One thread per item (a partition). The schema tolerates unknown keys so a
 *   later `also` can arrive without a version bump.
 * - Thread ids and singleton slugs share one URL space,
 *   /zeitgeist/meta/item/<id>. A slug that becomes a member keeps a redirect;
 *   `retiredIds` says which.
 */

import { z } from 'zod';
import { TIMESCALES, type Timescale } from './zeitgeist-parse';

// The trailing hyphen is legal: slugify truncates at 60 characters *after*
// trimming hyphens, so a long title can end on one, and those ids are live URLs.
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*-?$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const MAX_SLUG = 60;

export const ItemSlugSchema = z.string().regex(SLUG).max(MAX_SLUG).brand<'ItemSlug'>();
export const ThreadIdSchema = z.string().regex(SLUG).max(MAX_SLUG).brand<'ThreadId'>();
export type ItemSlug = z.infer<typeof ItemSlugSchema>;
export type ThreadId = z.infer<typeof ThreadIdSchema>;

export const ThreadSchema = z.object({
  id: ThreadIdSchema,
  /** A short noun phrase, as a reader would name the thing. Never a sentence. */
  title: z.string().min(1),
  /** Slugs of the items that belong to this thread. The id itself is implied. */
  members: z.array(ItemSlugSchema).readonly(),
  /** Date of the reading that explicitly closed the thread, if one did. */
  closed: z.string().regex(DATE).optional(),
});

export const RegistrySchema = z.object({
  version: z.literal(2),
  threads: z.array(ThreadSchema).readonly(),
});

export type Thread = z.infer<typeof ThreadSchema>;
export type Registry = z.infer<typeof RegistrySchema>;

export const EMPTY_REGISTRY: Registry = { version: 2, threads: [] };

/**
 * Item title → slug. Byte-identical to the shipped indexer, including its
 * truncate-after-trim order: slugs are public URLs and must not be tidied.
 */
export function slugify(text: string): ItemSlug {
  const slug = text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, MAX_SLUG);
  // Sound by construction: the replaces above emit exactly the SLUG alphabet.
  return slug as ItemSlug;
}

/** Parse untrusted JSON into a registry, or throw with zod's account of why not. */
export function parseRegistry(json: unknown): Registry {
  return RegistrySchema.parse(json);
}

/**
 * Structural faults zod cannot see: a slug claimed twice, a thread id that is
 * also some other thread's member, a duplicate thread id. Empty means sound.
 */
export function validateRegistry(registry: Registry): string[] {
  const problems: string[] = [];
  const owner = new Map<string, ThreadId>();
  const ids = new Set<string>();

  for (const thread of registry.threads) {
    if (ids.has(thread.id)) problems.push(`thread id "${thread.id}" is declared twice`);
    ids.add(thread.id);
  }

  for (const thread of registry.threads) {
    const seen = new Set<string>();
    for (const member of thread.members) {
      if (seen.has(member)) problems.push(`"${member}" is listed twice in "${thread.id}"`);
      seen.add(member);

      if (member === thread.id) problems.push(`"${thread.id}" lists itself as a member; the id is implied`);
      else if (ids.has(member)) problems.push(`"${member}" is a member of "${thread.id}" and also a thread id`);

      const previous = owner.get(member);
      if (previous !== undefined && previous !== thread.id) {
        problems.push(`"${member}" is claimed by both "${previous}" and "${thread.id}"`);
      }
      owner.set(member, thread.id);
    }
  }

  return problems;
}

export const THREAD_STATUSES = ['active', 'dormant', 'once', 'closed'] as const;
export type ThreadStatus = (typeof THREAD_STATUSES)[number];

/** A thread is active if it appeared in one of this many most recent readings. */
export const ACTIVE_WINDOW = 3;

/**
 * Where a thread stands. Counted in readings, not days: the cadence runs from
 * daily to three weeks apart, and "seen in the last three days" called almost
 * everything gone. `once` claims only what the archive knows, that an item
 * appeared one time; the label it replaces, "metabolised", claimed the
 * collective had digested it, of 98% of items, the war among them.
 */
export function statusOf(
  appearanceDates: readonly string[],
  readingDatesNewestFirst: readonly string[],
  closed?: string,
): ThreadStatus {
  if (closed !== undefined) return 'closed';
  const recent = new Set(readingDatesNewestFirst.slice(0, ACTIVE_WINDOW));
  if (appearanceDates.some(date => recent.has(date))) return 'active';
  return new Set(appearanceDates).size > 1 ? 'dormant' : 'once';
}

/**
 * The scales a thread has occupied, in the order it reached them, with
 * consecutive repeats collapsed: SURFACE, SURFACE, CURRENT, DEEP, CURRENT reads
 * as SURFACE → CURRENT → DEEP → CURRENT. A thread that appears at two scales in
 * one reading is ordered shallow to deep within that date. Length one means it
 * never moved.
 */
export function scaleTrajectory(
  appearances: readonly { readonly date: string; readonly timescale: Timescale }[],
): Timescale[] {
  const depth = (t: Timescale) => TIMESCALES.indexOf(t);
  const ordered = [...appearances].sort(
    (a, b) => a.date.localeCompare(b.date) || depth(a.timescale) - depth(b.timescale),
  );
  const trajectory: Timescale[] = [];
  for (const { timescale } of ordered) {
    if (trajectory.at(-1) !== timescale) trajectory.push(timescale);
  }
  return trajectory;
}

export interface Resolution {
  /** The thread the item belongs to, or the item's own slug if it stands alone. */
  readonly id: ThreadId | ItemSlug;
  /** The thread's title; null for an item that stands alone. */
  readonly title: string | null;
  readonly thread: Thread | null;
}

export interface ThreadResolver {
  resolve(slug: ItemSlug): Resolution;
  /** Member slugs: ids that used to be pages of their own and now redirect. */
  retiredIds(): ReadonlyMap<ItemSlug, ThreadId>;
  readonly registry: Registry;
}

/** Build an exact resolver. Throws if the registry is structurally unsound. */
export function buildResolver(registry: Registry): ThreadResolver {
  const problems = validateRegistry(registry);
  if (problems.length > 0) {
    throw new Error(`zeitgeist thread registry is unsound:\n- ${problems.join('\n- ')}`);
  }

  const bySlug = new Map<string, Thread>();
  const retired = new Map<ItemSlug, ThreadId>();
  for (const thread of registry.threads) {
    bySlug.set(thread.id, thread);
    for (const member of thread.members) {
      bySlug.set(member, thread);
      retired.set(member, thread.id);
    }
  }

  return {
    registry,
    retiredIds: () => retired,
    resolve(slug) {
      const thread = bySlug.get(slug) ?? null;
      return thread === null
        ? { id: slug, title: null, thread: null }
        : { id: thread.id, title: thread.title, thread };
    },
  };
}
