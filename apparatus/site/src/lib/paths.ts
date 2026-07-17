/**
 * Path resolution for the repository's content.
 *
 * The site is built from within its own directory (astro runs with cwd set to
 * the site root in both `dev` and `build`). Rather than count "../" hops from
 * there — which breaks the moment the site moves in the tree — we climb until
 * we find the repository root, identified by the top-level layout it must have:
 * a `corpus/` directory (the content) beside a `constellation/` directory (the
 * living graph). This survives the site living at ./site or ./apparatus/site.
 */

import fs from 'node:fs';
import path from 'node:path';

function findRepoRoot(start: string): string {
  let dir = start;
  for (let i = 0; i < 8; i++) {
    if (fs.existsSync(path.join(dir, 'corpus')) && fs.existsSync(path.join(dir, 'constellation'))) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  // Fall back to two levels up rather than throwing during early config
  // evaluation; a wrong guess surfaces immediately as a read miss.
  return path.resolve(start, '..');
}

export const REPO_ROOT = findRepoRoot(process.cwd());

/** The content library. All published documents live under here. */
export const CORPUS_ROOT = path.join(REPO_ROOT, 'corpus');

export function repoPath(...segments: string[]): string {
  return path.join(REPO_ROOT, ...segments);
}

/** Resolve a path inside the corpus. Corpus-relative paths ("synthesis/x.md")
 *  are also the public URL identity (/read/synthesis/x.md), so callers pass and
 *  store corpus-relative paths, and only join CORPUS_ROOT at the point of I/O. */
export function corpusPath(...segments: string[]): string {
  return path.join(CORPUS_ROOT, ...segments);
}
