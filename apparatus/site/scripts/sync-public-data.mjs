/**
 * Copy canonical corpus data into public/ before the build.
 *
 * The 3D explorer (public/explorer.html) is a static page that fetches its
 * graph at runtime, so it cannot import from src/lib the way the Astro pages
 * do. It previously read a copy of constellation.json that had been committed
 * by hand; that copy silently drifted 671 nodes behind canonical and froze in
 * a state that no longer parsed, which broke the explorer in production.
 *
 * Generating the copy each build keeps the explorer honest. The generated file
 * is gitignored — constellation/constellation.json is the only source.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const siteDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

// Climb to the repo root — the dir holding corpus/ beside constellation/ —
// rather than counting hops, so this survives the site moving in the tree.
function findRepoRoot(start) {
  let dir = start;
  for (let i = 0; i < 8; i++) {
    if (fs.existsSync(path.join(dir, 'corpus')) && fs.existsSync(path.join(dir, 'constellation'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error(`Could not locate repo root (corpus/ + constellation/) above ${start}`);
}

const repoRoot = findRepoRoot(siteDir);
const source = path.join(repoRoot, 'constellation', 'constellation.json');
const dest = path.join(siteDir, 'public', 'constellation.json');

const raw = fs.readFileSync(source, 'utf-8');

// Fail the build rather than ship a graph the explorer will choke on.
const parsed = JSON.parse(raw);
const nodeCount = Object.keys(parsed.nodes ?? {}).length;
if (nodeCount === 0) {
  throw new Error(`${source} parsed but contains no nodes — refusing to publish an empty graph.`);
}

fs.mkdirSync(path.dirname(dest), { recursive: true });
fs.writeFileSync(dest, raw, 'utf-8');

console.log(`[sync-public-data] constellation.json → public/ (${nodeCount} nodes)`);
