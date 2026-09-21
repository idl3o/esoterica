import type { APIRoute } from 'astro';
import { SITE_URL } from '../../lib/publish';
import { loadZeitgeist } from '../../lib/zeitgeist';
import { buildAtomFeed } from '../../lib/zeitgeist-feed';
import { extractCorrespondence, extractEdge } from '../../lib/zeitgeist-parse';

export const GET: APIRoute = () => {
  const entries = loadZeitgeist().map(reading => ({
    date: reading.date,
    headline: reading.headline,
    pattern: extractCorrespondence(reading.zeitMarkdown)?.pattern ?? null,
    edge: extractEdge(reading.zeitMarkdown),
    summary: reading.summary,
  }));

  return new Response(buildAtomFeed(entries, SITE_URL), {
    headers: { 'Content-Type': 'application/atom+xml; charset=utf-8' },
  });
};
