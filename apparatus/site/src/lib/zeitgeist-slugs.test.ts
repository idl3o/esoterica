import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
// The writer's helper is plain JS so a bare clone can run it. This test is what
// lets it repeat parser logic safely: it may never disagree with the site.
import { itemTitles, slugify as scriptSlugify } from '../../../scripts/zeitgeist-slugs.mjs';
import { corpusPath } from './paths';
import { TIMESCALES, extractItems, parseSection } from './zeitgeist-parse';
import { slugify } from './zeitgeist-threads';

describe('apparatus/scripts/zeitgeist-slugs.mjs agrees with the site', () => {
  const dir = corpusPath('synthesis', 'zeitgeist');
  const files = fs.readdirSync(dir).filter(f => /^zeitgeist-\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort();

  it.each(files)('%s: same items, same order, same slugs', f => {
    const md = fs.readFileSync(path.join(dir, f), 'utf-8');
    const site = TIMESCALES.flatMap(timescale =>
      extractItems(parseSection(md, timescale) ?? '').map(item => {
        const slug: string = slugify(item.title);
        return { timescale, title: item.title, slug };
      }),
    );
    const script = itemTitles(md).map(item => ({ ...item, slug: scriptSlugify(item.title) }));
    expect(script).toEqual(site);
  });

  it('slugifies awkward titles identically', () => {
    for (const title of ["Civilisation's floor: repriced!", 'aaaaaaaaa '.repeat(10), '— … —', 'Ünïcödé and 100% of $4,380/oz']) {
      expect(scriptSlugify(title)).toBe(slugify(title));
    }
  });
});
