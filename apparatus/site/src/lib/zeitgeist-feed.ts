/**
 * Atom feed of zeitgeist readings. Pure: entries in, XML out.
 *
 * Deterministic by construction: every timestamp derives from a reading's date,
 * never from the clock, so the same archive always builds the same feed and a
 * reader's client sees an entry change only when the entry changed.
 */

export interface FeedEntry {
  /** YYYY-MM-DD */
  readonly date: string;
  readonly headline: string;
  readonly pattern: string | null;
  readonly edge: string | null;
  readonly summary: string;
}

export const FEED_PATH = '/zeitgeist/feed.xml';
export const FEED_TITLE = 'Esoterica — Zeitgeist';
const FEED_SUBTITLE = 'Readings of the present moment, organised by the scale at which events metabolise.';
const DEFAULT_LIMIT = 20;

export function escapeXml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

const timestamp = (date: string) => `${date}T00:00:00Z`;

function entryXml(entry: FeedEntry, siteUrl: string): string {
  const url = `${siteUrl}/zeitgeist/${entry.date}`;
  const title = entry.headline.replace(/[.:]\s*$/, '') || `Reading of ${entry.date}`;
  const content = [
    entry.pattern === null ? null : `Correspondence: ${entry.pattern}`,
    entry.edge === null ? null : `The edge: ${entry.edge}`,
    entry.summary === '' ? null : entry.summary,
  ]
    .filter((part): part is string => part !== null)
    .join('\n\n');

  return [
    '  <entry>',
    `    <id>${escapeXml(url)}</id>`,
    `    <title>${escapeXml(title)}</title>`,
    `    <link rel="alternate" type="text/html" href="${escapeXml(url)}"/>`,
    `    <published>${timestamp(entry.date)}</published>`,
    `    <updated>${timestamp(entry.date)}</updated>`,
    `    <summary>${escapeXml(entry.summary)}</summary>`,
    `    <content type="text">${escapeXml(content)}</content>`,
    '  </entry>',
  ].join('\n');
}

/** Newest first, capped at `limit`. `siteUrl` has no trailing slash. */
export function buildAtomFeed(entries: readonly FeedEntry[], siteUrl: string, limit = DEFAULT_LIMIT): string {
  const newestFirst = [...entries].sort((a, b) => b.date.localeCompare(a.date)).slice(0, limit);
  const updated = newestFirst[0]?.date ?? '1970-01-01';

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">',
    `  <id>${escapeXml(siteUrl + FEED_PATH)}</id>`,
    `  <title>${escapeXml(FEED_TITLE)}</title>`,
    `  <subtitle>${escapeXml(FEED_SUBTITLE)}</subtitle>`,
    `  <link rel="self" type="application/atom+xml" href="${escapeXml(siteUrl + FEED_PATH)}"/>`,
    `  <link rel="alternate" type="text/html" href="${escapeXml(`${siteUrl}/zeitgeist`)}"/>`,
    `  <updated>${timestamp(updated)}</updated>`,
    '  <author><name>Esoterica</name></author>',
    ...newestFirst.map(entry => entryXml(entry, siteUrl)),
    '</feed>',
    '',
  ].join('\n');
}
