import type { APIRoute } from 'astro';
import { loadLibraryIndex } from '../lib/content';
import {
  LIBRARY_LICENSE, THIRD_PARTY_LICENSE, SITE_URL,
  getAttribution, isThirdParty, licenseFor,
} from '../lib/publish';

/**
 * The whole catalogue as one document. A library that says "take what is
 * useful" needs a way to take it that isn't scraping rendered HTML.
 *
 * Licence is per-document, not blanket: see lib/publish.ts.
 */
export const GET: APIRoute = () => {
  const docs = loadLibraryIndex().map(d => {
    const source = d.readPath.replace(/^\/read\//, '');
    const attribution = getAttribution(source);
    return {
      title: d.title,
      subtitle: d.subtitle || undefined,
      collection: d.source,
      category: d.category || undefined,
      wordCount: d.wordCount,
      readingTime: d.readingTime,
      html: `${SITE_URL}${d.readPath}`,
      markdown: `${SITE_URL}/raw/${source}`,
      source,
      license: licenseFor(source),
      ...(attribution && {
        transcriptOf: { url: attribution.url, title: attribution.title, channel: attribution.channel },
      }),
    };
  });

  const own = docs.filter(d => !isThirdParty(d.source));

  return new Response(
    JSON.stringify(
      {
        library: 'Esoterica',
        license: {
          default: LIBRARY_LICENSE,
          note:
            'Documents carrying a `transcriptOf` field are machine transcripts of third-party ' +
            'recordings. They are published with attribution but are not the library\'s to licence: ' +
            THIRD_PARTY_LICENSE + '. Every other document is ' + LIBRARY_LICENSE + '.',
        },
        documents: docs.length,
        ownDocuments: own.length,
        words: docs.reduce((n, d) => n + d.wordCount, 0),
        catalogue: docs,
      },
      null,
      2,
    ),
    { headers: { 'Content-Type': 'application/json; charset=utf-8' } },
  );
};
