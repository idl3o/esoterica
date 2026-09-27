import { describe, expect, it } from 'vitest';
import { buildAtomFeed, escapeXml, type FeedEntry } from './zeitgeist-feed';

const entry = (date: string, over: Partial<FeedEntry> = {}): FeedEntry => ({
  date,
  headline: 'The brake was filed as a cartel.',
  pattern: 'stopping distance',
  edge: 'What presses is custody.',
  summary: 'Metta-darshan first...',
  ...over,
});

const SITE = 'https://esoterica.example';

describe('buildAtomFeed', () => {
  it('lists newest first whatever order it is given, and caps at the limit', () => {
    const xml = buildAtomFeed([entry('2026-09-04'), entry('2026-09-19'), entry('2026-09-10')], SITE, 2);
    const ids = [...xml.matchAll(/<entry>\s*<id>([^<]+)<\/id>/g)].map(m => m[1]);
    expect(ids).toEqual([`${SITE}/zeitgeist/2026-09-19`, `${SITE}/zeitgeist/2026-09-10`]);
  });

  it('takes every timestamp from a reading date, never the clock', () => {
    const entries = [entry('2026-09-19'), entry('2026-09-10')];
    const xml = buildAtomFeed(entries, SITE);
    expect(xml).toBe(buildAtomFeed(entries, SITE));
    expect(xml).toContain('<updated>2026-09-19T00:00:00Z</updated>');
    expect([...xml.matchAll(/T\d\d:\d\d:\d\dZ/g)].every(m => m[0] === 'T00:00:00Z')).toBe(true);
  });

  it('escapes markup and quotes in every text field', () => {
    const xml = buildAtomFeed([entry('2026-09-19', {
      headline: 'Fish & "nets" <too> big',
      pattern: "the net's <mesh>",
      edge: 'a & b',
      summary: '5 < 6 & "so on"',
    })], SITE);
    expect(xml).toContain('<title>Fish &amp; &quot;nets&quot; &lt;too&gt; big</title>');
    expect(xml).toContain('Correspondence: the net&apos;s &lt;mesh&gt;');
    expect(xml).not.toMatch(/<too>|<mesh>/);
    expect(escapeXml('&amp;')).toBe('&amp;amp;');
  });

  it('drops the headline’s closing stop, and survives a reading with no pattern, edge or headline', () => {
    expect(buildAtomFeed([entry('2026-09-19')], SITE)).toContain('<title>The brake was filed as a cartel</title>');
    const bare = buildAtomFeed([entry('2026-02-16', { headline: '', pattern: null, edge: null, summary: '' })], SITE);
    expect(bare).toContain('<title>Reading of 2026-02-16</title>');
    expect(bare).toContain('<content type="text"></content>');
  });

  it('is a well-formed empty feed when there are no readings', () => {
    const xml = buildAtomFeed([], SITE);
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom"')).toBe(true);
    expect(xml.trimEnd().endsWith('</feed>')).toBe(true);
    expect(xml).not.toContain('<entry>');
  });

  it('balances every element it opens', () => {
    const xml = buildAtomFeed([entry('2026-09-19'), entry('2026-09-10')], SITE);
    for (const tag of ['feed', 'entry', 'id', 'title', 'summary', 'content', 'updated', 'published', 'author', 'name', 'subtitle']) {
      const open = [...xml.matchAll(new RegExp(`<${tag}[ >]`, 'g'))].length;
      const close = [...xml.matchAll(new RegExp(`</${tag}>`, 'g'))].length;
      expect(open, tag).toBe(close);
    }
  });
});
