/**
 * Wiki-link resolver — renders `[[slug]]` citations as links into /read/.
 *
 * The corpus's harvest documents cite each other with Obsidian-style
 * `[[slug]]` and `[[slug|label]]` links. Marked does not know them, so until
 * now every one rendered as literal brackets. This is the site-side twin of
 * `apparatus/scripts/linkgraph.py`; the two must apply the same rulings
 * (corpus/seeds/SEED-HARVEST-2026-09.md, "RULINGS"):
 *
 *   path-like target        <target>.md, corpus-relative
 *   slug.seed/.grown/.slate explicit class
 *   bare slug               grown synthesis > seed > unique other; slate never
 *   snake_case              constellation node -> its document
 *   Title Case prose        slugified, then the rules above
 *   ALIASES                 near-miss retargets
 *
 * Runs on the markdown before `marked.parse`, and emits `/read/` hrefs that
 * `rewriteDocLinks` leaves untouched. Unresolved targets keep their label and
 * take the same `dead-link` class as an unpublished relative link.
 */

import { getPublishedPaths } from './content';
import { getAllNodes } from './constellation';
import { loadLinkRules } from './link-rules';

const WIKI = /\[\[([^\]|#]+)(?:\|([^\]]*))?(?:#[^\]]*)?\]\]/g;
const FENCE = /(```[\s\S]*?```|`[^`\n]*`)/g;

// The alias table, bare-slug preferences and directory tie-break order are
// shared with the harness through apparatus/scripts/link-rules.json.
const { aliases: ALIASES, prefer: PREFER, dir_priority: DIR_PRIORITY } = loadLinkRules();

type DocClass = 'grown' | 'seed' | 'slate' | 'other';

function docClass(p: string): DocClass {
  if (p.startsWith('synthesis/grown/')) return 'grown';
  if (p.startsWith('seeds/')) return 'seed';
  if (p.startsWith('film-slate/')) return 'slate';
  return 'other';
}

function slugOf(p: string): string {
  let stem = p.split('/').pop()!.replace(/\.md$/, '');
  if (docClass(p) === 'slate') stem = stem.replace(/^\d+-/, '');
  return stem;
}

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
}

let _bySlug: Map<string, string[]> | null = null;

function bySlug(): Map<string, string[]> {
  if (_bySlug) return _bySlug;
  _bySlug = new Map();
  for (const p of getPublishedPaths()) {
    const s = slugOf(p);
    if (!_bySlug.has(s)) _bySlug.set(s, []);
    _bySlug.get(s)!.push(p);
  }
  for (const list of _bySlug.values()) list.sort();
  return _bySlug;
}

function pick(candidates: string[], want: DocClass | null): string | null {
  if (want) return candidates.find(c => docClass(c) === want) ?? null;
  for (const cls of ['grown', 'seed'] as const) {
    const hit = candidates.find(c => docClass(c) === cls);
    if (hit) return hit;
  }
  const others = candidates.filter(c => docClass(c) === 'other');
  if (others.length === 0) return null;
  if (others.length === 1) return others[0];
  const preferred = PREFER[slugOf(others[0])];
  if (preferred && others.includes(preferred)) return preferred;
  for (const prefix of DIR_PRIORITY) {
    const hit = others.find(c => c.startsWith(prefix));
    if (hit) return hit;
  }
  return others[0];
}

/** Resolve one wiki-link target to a published corpus-relative path, or null. */
export function resolveWikiLink(target: string): string | null {
  const published = getPublishedPaths();
  let t = target.trim().replace(/^\.?\//, '');
  if (t.includes('/')) {
    const cand = t.replace(/\.md$/, '') + '.md';
    return published.has(cand) ? cand : null;
  }
  let want: DocClass | null = null;
  const m = t.match(/^(.+)\.(seed|grown|slate)$/);
  if (m) { t = m[1]; want = m[2] as DocClass; }
  if (!bySlug().has(t) && /[A-Z\s]/.test(t)) t = slugify(t);
  t = ALIASES[t] ?? t;
  const candidates = bySlug().get(t) ?? (t.includes('_') ? bySlug().get(t.replace(/_/g, '-')) : undefined);
  if (candidates) return pick(candidates, want);
  const node = getAllNodes()[t.replace(/-/g, '_')];
  if (node?.document && published.has(node.document)) return node.document;
  return null;
}

function label(target: string, given?: string): string {
  if (given && given.trim()) return given.trim();
  return target.trim().replace(/\.(seed|grown|slate)$/, '').replace(/^.*\//, '').replace(/-/g, ' ');
}

function escape(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/**
 * Replace every `[[…]]` in a markdown document with a link into the published
 * corpus. Code spans and fenced blocks are left alone.
 */
export function expandWikiLinks(markdown: string): string {
  return markdown.split(FENCE).map((part, i) => {
    if (i % 2 === 1) return part;
    return part.replace(WIKI, (_m, target: string, given?: string) => {
      const text = escape(label(target, given));
      const path = resolveWikiLink(target);
      if (!path) return `<a class="dead-link" title="Not yet in the library">${text}</a>`;
      return `<a href="/read/${path}">${text}</a>`;
    });
  }).join('');
}
