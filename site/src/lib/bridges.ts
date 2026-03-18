/**
 * Fiction bridge metadata extraction.
 * Reads fiction-bridges/*.md and extracts title, subtitle, quote, word count.
 */

import fs from 'node:fs';
import path from 'node:path';
import { repoPath } from './paths';

export interface BridgeMeta {
  slug: string;
  filename: string;
  title: string;
  subtitle: string;
  quote: string;
  wordCount: number;
  readingTime: number;
  franchise: string;
}

let _cached: BridgeMeta[] | null = null;

/** Extract a franchise label from the bridge title or slug */
function extractFranchise(title: string, slug: string): string {
  const map: [RegExp, string][] = [
    [/star trek/i, 'Star Trek'],
    [/elden ring/i, 'Elden Ring'],
    [/dragon\s?ball/i, 'Dragon Ball'],
    [/sailor moon/i, 'Sailor Moon'],
    [/arcane/i, 'Arcane'],
    [/drizzt|underdark/i, 'Forgotten Realms'],
    [/one piece|shanks|buggy/i, 'One Piece'],
    [/naruto/i, 'Naruto'],
    [/sun wukong|journey to the west|stone to buddha/i, 'Journey to the West'],
    [/marvel|beyonder|kang|apocalypse|namor/i, 'Marvel'],
    [/moon\s?knight|khonshu/i, 'Marvel'],
    [/fermionic|galactic center/i, 'Cosmology'],
    [/cosmic censure/i, 'Cosmology'],
    [/unified field/i, 'Meta'],
  ];

  const combined = `${title} ${slug}`;
  for (const [pattern, franchise] of map) {
    if (pattern.test(combined)) return franchise;
  }
  return 'Esoterica';
}

export function loadBridges(): BridgeMeta[] {
  if (_cached) return _cached;

  const bridgesDir = repoPath('fiction-bridges');
  let files: string[];
  try {
    files = fs.readdirSync(bridgesDir).filter(f => f.endsWith('.md'));
  } catch {
    return [];
  }

  const bridges: BridgeMeta[] = [];

  for (const file of files) {
    const content = fs.readFileSync(path.join(bridgesDir, file), 'utf-8');
    const lines = content.split('\n');

    const title = lines.find(l => l.startsWith('# '))?.replace(/^#\s*/, '') || file;
    const subtitle = lines.find(l => l.startsWith('## '))?.replace(/^##\s*/, '') || '';

    // Extract first blockquote
    const quoteLines: string[] = [];
    let inQuote = false;
    for (const line of lines) {
      if (line.startsWith('> ')) {
        inQuote = true;
        quoteLines.push(line.replace(/^>\s*/, ''));
      } else if (inQuote) {
        break;
      }
    }
    const quote = quoteLines.join(' ').replace(/\*([^*]+)\*/g, '$1').substring(0, 200);

    const wordCount = content.split(/\s+/).length;
    const slug = file.replace('.md', '');

    bridges.push({
      slug,
      filename: file,
      title,
      subtitle,
      quote: quote || '',
      wordCount,
      readingTime: Math.ceil(wordCount / 250),
      franchise: extractFranchise(title, slug),
    });
  }

  // Sort: larger/newer bridges first (by word count as proxy for depth)
  bridges.sort((a, b) => b.wordCount - a.wordCount);

  _cached = bridges;
  return bridges;
}

/** Read the full markdown content of a bridge */
export function readBridgeContent(slug: string): string | null {
  const bridgesDir = repoPath('fiction-bridges');
  const filePath = path.join(bridgesDir, `${slug}.md`);
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch {
    return null;
  }
}
