/**
 * Path resolution for content directories.
 * The repository root is always one level up from the site/ directory.
 * Works in both dev mode and build mode.
 */

import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve from this file → site/src/lib/ → site/ → repo root
const thisDir = path.dirname(fileURLToPath(import.meta.url));

// In dev: thisDir = site/src/lib
// In build: thisDir = site/dist/.prerender/chunks (or similar)
// So we use process.cwd() which is always site/ during both dev and build
const siteDir = process.cwd();

// Repository root is one level up from site/
export const REPO_ROOT = path.resolve(siteDir, '..');

export function repoPath(...segments: string[]): string {
  return path.join(REPO_ROOT, ...segments);
}
