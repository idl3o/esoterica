import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { z } from 'zod';
import { corpusPath, repoPath } from './paths';
import { TIMESCALES, extractItems, parseSection } from './zeitgeist-parse';
import {
  ItemSlugSchema,
  buildResolver,
  parseRegistry,
  scaleTrajectory,
  slugify,
  statusOf,
  validateRegistry,
  type Registry,
} from './zeitgeist-threads';

const registry = (threads: readonly { id: string; title: string; members: readonly string[]; closed?: string }[]): Registry =>
  parseRegistry({ version: 2, threads });

describe('slugify', () => {
  it('lowercases, hyphenates and trims', () => {
    expect(slugify("The Oil Shock: Civilisation's Floor!")).toBe('the-oil-shock-civilisation-s-floor');
  });

  it('truncates at 60 after trimming, so a long title may end on a hyphen (live URLs depend on it)', () => {
    const slug = slugify('The inference economy is a civilisational pivot that is being priced');
    expect(slug).toHaveLength(60);
    expect(slug).toBe('the-inference-economy-is-a-civilisational-pivot-that-is-bein');
    expect(slugify('aaaaaaaaa '.repeat(10))).toMatch(/-$/);
  });

  it('yields an empty slug for a title with no ASCII letters or digits, which the schema rejects', () => {
    expect(slugify('— … —')).toBe('');
    expect(ItemSlugSchema.safeParse('').success).toBe(false);
  });
});

describe('validateRegistry', () => {
  it('passes a sound registry', () => {
    expect(validateRegistry(registry([{ id: 'iran-war', title: 'The Iran War', members: ['the-war-unnamed'] }]))).toEqual([]);
  });

  it('names a slug claimed by two threads', () => {
    const problems = validateRegistry(registry([
      { id: 'iran-war', title: 'The Iran War', members: ['a-strait-sets-the-price'] },
      { id: 'rate-cycle', title: 'The Rate Cycle', members: ['a-strait-sets-the-price'] },
    ]));
    expect(problems).toEqual(['"a-strait-sets-the-price" is claimed by both "iran-war" and "rate-cycle"']);
  });

  it('names a duplicate thread id, a self-member, a repeated member and a member that is a thread id', () => {
    const problems = validateRegistry(registry([
      { id: 'iran-war', title: 'The Iran War', members: ['iran-war', 'x-item', 'x-item', 'rate-cycle'] },
      { id: 'rate-cycle', title: 'The Rate Cycle', members: [] },
      { id: 'rate-cycle', title: 'Again', members: [] },
    ]));
    expect(problems).toContain('thread id "rate-cycle" is declared twice');
    expect(problems).toContain('"iran-war" lists itself as a member; the id is implied');
    expect(problems).toContain('"x-item" is listed twice in "iran-war"');
    expect(problems).toContain('"rate-cycle" is a member of "iran-war" and also a thread id');
  });

  it('rejects malformed input at the schema', () => {
    expect(() => parseRegistry({ version: 1, merges: [] })).toThrow();
    expect(() => registry([{ id: 'Iran War', title: 'x', members: [] }])).toThrow();
    expect(() => registry([{ id: 'iran-war', title: '', members: [] }])).toThrow();
    expect(() => registry([{ id: 'iran-war', title: 'x', members: [], closed: 'September' }])).toThrow();
  });
});

describe('buildResolver', () => {
  const resolver = buildResolver(registry([
    { id: 'oil-shock', title: 'The Oil Shock', members: ['the-oil-shock-is-repricing-the-world'] },
  ]));

  it('resolves a member and the thread id itself to the thread', () => {
    expect(resolver.resolve(slugify('The oil shock is repricing the world')).id).toBe('oil-shock');
    expect(resolver.resolve(slugify('Oil shock')).title).toBe('The Oil Shock');
  });

  it('leaves an unlisted item alone, even when its title contains a thread title', () => {
    const r = resolver.resolve(slugify('After the oil shock, a quieter week'));
    expect(r.id).toBe('after-the-oil-shock-a-quieter-week');
    expect(r.title).toBeNull();
    expect(r.thread).toBeNull();
  });

  it('reports which ids were retired into threads', () => {
    expect([...resolver.retiredIds()]).toEqual([['the-oil-shock-is-repricing-the-world', 'oil-shock']]);
  });

  it('refuses an unsound registry, loudly', () => {
    expect(() => buildResolver(registry([
      { id: 'a-thread', title: 'A', members: ['shared-item'] },
      { id: 'b-thread', title: 'B', members: ['shared-item'] },
    ]))).toThrow(/unsound[\s\S]*shared-item/);
  });
});

describe('statusOf', () => {
  const readings = ['2026-09-19', '2026-09-10', '2026-09-04', '2026-08-13', '2026-07-28'];

  it('is active when seen in one of the three most recent readings, however many days ago that was', () => {
    expect(statusOf(['2026-09-04'], readings)).toBe('active');
    expect(statusOf(['2026-03-03', '2026-09-19'], readings)).toBe('active');
  });

  it('is dormant when it recurred and then fell out of the window', () => {
    expect(statusOf(['2026-07-28', '2026-08-13'], readings)).toBe('dormant');
  });

  it('is once, not "metabolised", when it appeared a single time and left', () => {
    expect(statusOf(['2026-08-13'], readings)).toBe('once');
    expect(statusOf(['2026-08-13', '2026-08-13'], readings)).toBe('once');
  });

  it('is closed only when a reading closed it, whatever else is true', () => {
    expect(statusOf(['2026-09-19'], readings, '2026-09-19')).toBe('closed');
  });

  it('calls everything active while the archive is shorter than the window', () => {
    expect(statusOf(['2026-09-19'], ['2026-09-19'])).toBe('active');
  });
});

describe('scaleTrajectory', () => {
  it('collapses consecutive repeats and keeps returns', () => {
    expect(scaleTrajectory([
      { date: '2026-03-03', timescale: 'SURFACE' },
      { date: '2026-03-10', timescale: 'SURFACE' },
      { date: '2026-03-18', timescale: 'DEEP' },
      { date: '2026-04-09', timescale: 'TECTONIC' },
      { date: '2026-05-01', timescale: 'DEEP' },
    ])).toEqual(['SURFACE', 'DEEP', 'TECTONIC', 'DEEP']);
  });

  it('orders by date whatever order it is given, and shallow to deep within one reading', () => {
    expect(scaleTrajectory([
      { date: '2026-09-10', timescale: 'DEEP' },
      { date: '2026-09-10', timescale: 'SURFACE' },
      { date: '2026-09-04', timescale: 'CURRENT' },
    ])).toEqual(['CURRENT', 'SURFACE', 'DEEP']);
  });

  it('has length one for a thread that never moved, and zero for none', () => {
    expect(scaleTrajectory([{ date: '2026-09-19', timescale: 'CURRENT' }, { date: '2026-09-10', timescale: 'CURRENT' }])).toEqual(['CURRENT']);
    expect(scaleTrajectory([])).toEqual([]);
  });
});

/** The committed registry, held against the committed archive. */
describe('the registry on disk', () => {
  const data = (f: string): unknown => JSON.parse(fs.readFileSync(repoPath('apparatus', 'site', 'src', 'data', f), 'utf-8'));
  const onDisk = parseRegistry(data('zeitgeist-threads.json'));
  const resolver = buildResolver(onDisk);

  const dir = corpusPath('synthesis', 'zeitgeist');
  const archiveSlugs = new Set<string>();
  for (const f of fs.readdirSync(dir).filter(n => /^zeitgeist-\d{4}-\d{2}-\d{2}\.md$/.test(n))) {
    const md = fs.readFileSync(path.join(dir, f), 'utf-8');
    for (const timescale of TIMESCALES) {
      for (const item of extractItems(parseSection(md, timescale) ?? '')) archiveSlugs.add(slugify(item.title));
    }
  }

  it('is sound', () => {
    expect(validateRegistry(onDisk)).toEqual([]);
  });

  it('has no dangling member: every slug it lists is an item in some reading', () => {
    const dangling = onDisk.threads.flatMap(t => t.members.filter(m => !archiveSlugs.has(m)).map(m => `${t.id} <- ${m}`));
    expect(dangling).toEqual([]);
  });

  it('gives every archive item a slug the schema accepts', () => {
    const bad = [...archiveSlugs].filter(s => !ItemSlugSchema.safeParse(s).success);
    expect(bad).toEqual([]);
  });

  it('names threads as short noun phrases, not sentences', () => {
    const sentences = onDisk.threads.filter(t => t.title.split(/\s+/).length > 6 || /[.!?]$/.test(t.title)).map(t => t.title);
    expect(sentences).toEqual([]);
  });

  /**
   * Item URLs are public. Every id that was live when the snapshot was taken
   * must still be a page (a live id) or a redirect (a retired member).
   */
  it('keeps every snapshotted item URL alive, as a page or a redirect', () => {
    const snapshot = z.object({ ids: z.array(z.string()) }).parse(data('zeitgeist-item-ids.snapshot.json'));
    const live = new Set([...archiveSlugs].map((s): string => resolver.resolve(ItemSlugSchema.parse(s)).id));
    const retired = new Set<string>(resolver.retiredIds().keys());
    const dead = snapshot.ids.filter(id => !live.has(id) && !retired.has(id));
    expect(snapshot.ids.length).toBeGreaterThanOrEqual(402);
    expect(dead).toEqual([]);
  });
});
