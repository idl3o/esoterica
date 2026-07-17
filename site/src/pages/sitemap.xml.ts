import type { APIRoute } from 'astro';
import { loadLibraryIndex, loadSynthesisIndex } from '../lib/content';
import { loadBridges } from '../lib/bridges';
import { getAllNodes } from '../lib/constellation';
import { SITE_URL } from '../lib/publish';

const escape = (s: string) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');

export const GET: APIRoute = () => {
  const urls: { loc: string; priority: string }[] = [];
  const add = (loc: string, priority = '0.5') => urls.push({ loc, priority });

  add('/', '1.0');
  for (const p of ['/library', '/explorer', '/wander', '/bridges', '/zeitgeist']) add(p, '0.8');

  for (const doc of loadLibraryIndex()) add(doc.readPath, '0.7');
  for (const bridge of loadBridges()) add(`/bridges/${bridge.slug}`, '0.7');
  for (const id of Object.keys(getAllNodes())) add(`/node/${encodeURIComponent(id)}`, '0.4');

  const seen = new Set<string>();
  const body = urls
    .filter(u => !seen.has(u.loc) && seen.add(u.loc))
    .map(u => `  <url>\n    <loc>${escape(SITE_URL + u.loc)}</loc>\n    <priority>${u.priority}</priority>\n  </url>`)
    .join('\n');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
};
