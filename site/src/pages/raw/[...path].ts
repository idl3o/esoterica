import type { APIRoute } from 'astro';
import { getAllContentPaths, readContent } from '../../lib/content';

/** Every published document as its own markdown source, at /raw/<path>. */
export function getStaticPaths() {
  return getAllContentPaths().map(p => ({
    params: { path: p.path },
    props: { contentPath: p.path },
  }));
}

export const GET: APIRoute = ({ props }) => {
  const markdown = readContent((props as { contentPath: string }).contentPath);
  if (markdown === null) return new Response('Not found', { status: 404 });

  return new Response(markdown, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
    },
  });
};
