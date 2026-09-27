#!/usr/bin/env node
/**
 * zeitgeist-slugs — list a reading's items with their slugs and current threads.
 *
 *   node apparatus/scripts/zeitgeist-slugs.mjs corpus/synthesis/zeitgeist/zeitgeist-2026-09-19.md
 *   node apparatus/scripts/zeitgeist-slugs.mjs --threads        # the registry, one line per thread
 *
 * For the writer of a reading (Step 3c of /zeitgeist): slugs are what the thread
 * registry is keyed by, and a slug computed by eye is a slug computed wrong.
 *
 * Dependency-free on purpose, so the cloud routine can run it on a bare clone.
 * That means it repeats two small pieces of the site's parser. They cannot
 * drift: apparatus/site/src/lib/zeitgeist-slugs.test.ts holds `slugify` and
 * `itemTitles` to the site's own implementations over the whole archive.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const TIMESCALES = ['SURFACE', 'CURRENT', 'DEEP', 'TECTONIC'];
const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const REGISTRY = path.join(REPO, 'apparatus', 'site', 'src', 'data', 'zeitgeist-threads.json');

/** Byte-identical to the site's slugify: slugs are public URLs. */
export function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').substring(0, 60);
}

/** Item titles of one reading, by timescale, as the site extracts them. */
export function itemTitles(markdown) {
  const md = markdown.replace(/\r\n/g, '\n');
  const out = [];
  for (const timescale of TIMESCALES) {
    const section = new RegExp(`(?:^|\\n)## ${timescale}[^\\n]*\\n+(?:\\*[^*\\n]+\\*[ \\t]*\\n)?([\\s\\S]*?)(?=\\n## |$)`, 'i').exec(md)?.[1];
    if (section === undefined) continue;
    const content = section.replace(/\n(?:-{3,}[ \t]*\n+)?Sources:[\s\S]*$/, '').replace(/\n+-{3,}\s*$/, '').trim();
    for (const m of content.matchAll(/\*\*([^*]+?)[.:]?\*\*\.?\s*([\s\S]*?)(?=\n\n(?:- )?\*\*[^*]+\*\*|$)/g)) {
      const title = (m[1] ?? '').trim();
      if (title.length >= 5) out.push({ timescale, title });
    }
  }
  return out;
}

function loadRegistry() {
  return fs.existsSync(REGISTRY) ? JSON.parse(fs.readFileSync(REGISTRY, 'utf-8')) : { version: 2, threads: [] };
}

function main(argv) {
  const registry = loadRegistry();
  if (argv[0] === '--threads') {
    for (const t of registry.threads) console.log(`${t.id}\t${t.title}\t${t.members.length + 1} slug(s)${t.closed ? `\tclosed ${t.closed}` : ''}`);
    return 0;
  }
  if (argv.length !== 1) {
    console.error('usage: zeitgeist-slugs.mjs <reading.md> | --threads');
    return 2;
  }
  const owner = new Map();
  for (const t of registry.threads) {
    owner.set(t.id, t.id);
    for (const m of t.members) owner.set(m, t.id);
  }
  for (const { timescale, title } of itemTitles(fs.readFileSync(argv[0], 'utf-8'))) {
    const slug = slugify(title);
    console.log(`${timescale}\t${owner.get(slug) ?? '(standalone)'}\t${slug}\t${title}`);
  }
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = main(process.argv.slice(2));
}
