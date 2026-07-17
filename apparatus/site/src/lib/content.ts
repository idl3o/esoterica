/**
 * Content loader — reads markdown documents from all content directories.
 * Port of build-synthesis-index.js logic for Astro's build-time data pipeline.
 */

import fs from 'node:fs';
import path from 'node:path';
import { CORPUS_ROOT } from './paths';
import { loadConstellation } from './constellation';
import { buildDocumentNodeLinks, type DocumentMeta, type DocumentNodeLinks } from './document-links';

// --- Types ---

export interface ContentDocument extends DocumentMeta {
  fileName: string;
  subtitle: string;
  excerpt: string;
  wordCount: number;
  quotes: string[];
  structure: { level: number; heading: string }[];
  sourceDir: string;
}

export interface LibraryDocument {
  title: string;
  subtitle: string;
  category: string;
  wordCount: number;
  readingTime: number;
  readPath: string;
  source: string;
  sourceDir: string;
}

// --- Constants ---

// Paths are corpus-relative throughout — "synthesis/x.md", which is also the
// public URL identity — so every read joins the corpus root here.
const ROOT = CORPUS_ROOT;

/**
 * The corpus. One list, used for both the /read/ routes and the synthesis
 * index that links to them — if a directory is indexed but not routed, every
 * link into it 404s.
 *
 * `world-model/` is deliberately absent: it is a Python project whose only
 * markdown is its own README and ARCHITECTURE. Apparatus, not corpus.
 */
const CORPUS_DIRS = [
  { dir: 'synthesis', label: 'Synthesis' },
  { dir: 'distillations', label: 'Distillations' },
  { dir: 'protocols', label: 'Protocols' },
  { dir: 'seeds', label: 'Seeds' },
  { dir: 'traditions', label: 'Traditions' },
  { dir: 'translated', label: 'Translated' },
  { dir: 'extractions', label: 'Extractions' },
  { dir: 'correspondences', label: 'Correspondences' },
  { dir: 'journey', label: 'Journey' },
  { dir: 'garden', label: 'Garden' },
  { dir: 'harvest', label: 'Harvest' },
  { dir: 'world-tree', label: 'World Tree' },
  { dir: 'memory-palace', label: 'Memory Palace' },
  { dir: 'misc', label: 'Misc' },
  { dir: 'fiction-bridges', label: 'Fiction Bridges' },
  { dir: 'film-slate', label: 'Film Slate' },
  { dir: 'voices', label: 'Voices' },
  { dir: 'negative-space', label: 'Negative Space' },
  { dir: 'audio-transcripts', label: 'Audio Transcripts' },
];

/** Withheld from publication. Must match across routing and indexing. */
const EXCLUDED_SUBDIRS = new Set(['internal', 'personal']);

const TERM_PATTERNS = [
  'consciousness', 'awareness', 'recognition', 'polarity', 'density',
  'wanderer', 'service', 'manifestation', 'timeline', 'synchronicity',
  'archetype', 'apollo', 'mercury', 'kalki', 'samael',
  'singularity', 'galactic', 'cosmic', 'source', 'unity',
  'sacred geometry', 'fibonacci', 'reality programming',
  'love-light', 'frequency', 'resonance', 'vibration',
  'enlightenment', 'awakening', 'breakthrough', 'integration'
];

// --- Caches ---

let _synthesisIndex: ContentDocument[] | null = null;
let _libraryIndex: LibraryDocument[] | null = null;
let _documentLinks: DocumentNodeLinks | null = null;

// --- Parsing ---

function scanDir(dir: string, fileList: string[] = []): string[] {
  if (!fs.existsSync(dir)) return fileList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !entry.name.startsWith('.') && !EXCLUDED_SUBDIRS.has(entry.name)) {
      scanDir(fullPath, fileList);
    } else if (entry.name.endsWith('.md') && entry.name !== 'README.md') {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

function generateId(fileName: string): string {
  return fileName.replace('.md', '').replace(/[^a-z0-9]+/gi, '-').toLowerCase().replace(/^-|-$/g, '');
}

function extractTags(content: string, category: string): string[] {
  const tags = new Set<string>();
  const lower = content.toLowerCase();
  for (const term of TERM_PATTERNS) {
    if (lower.includes(term.toLowerCase())) tags.add(term);
  }
  if (category) tags.add(category);
  return Array.from(tags).slice(0, 12);
}

function parseDocument(filePath: string, content: string): ContentDocument {
  const lines = content.split('\n');
  const relPath = path.relative(ROOT, filePath).replace(/\\/g, '/');

  // Determine source/category
  const parts = relPath.split('/');
  let source = 'synthesis';
  let category = 'uncategorized';
  let sourceDir = parts[0] || 'synthesis';

  if (parts.includes('extractions')) {
    source = 'extraction';
    category = 'extraction';
  } else if (parts.includes('translated')) {
    source = 'translated';
    category = 'translated';
  } else if (parts.includes('synthesis')) {
    const idx = parts.indexOf('synthesis');
    if (parts.length > idx + 2) category = parts[idx + 1];
  }

  let title = '';
  let subtitle = '';
  const quotes: string[] = [];
  const structure: { level: number; heading: string }[] = [];
  const excerptCandidates: string[] = [];
  let inFrontmatter = false;
  let pastFrontmatter = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // Skip frontmatter
    if (trimmed === '---') {
      if (!pastFrontmatter && !inFrontmatter) { inFrontmatter = true; continue; }
      if (inFrontmatter) { inFrontmatter = false; pastFrontmatter = true; continue; }
    }
    if (inFrontmatter) continue;

    if (!title && trimmed.startsWith('# ')) {
      title = trimmed.substring(2).trim();
      continue;
    }
    if (!subtitle && trimmed.startsWith('## ')) {
      subtitle = trimmed.substring(3).trim();
    }

    if (trimmed.startsWith('> ') && trimmed.length > 10) {
      const q = trimmed.substring(2).trim();
      if (q.length > 20 && q.length < 200) quotes.push(q);
    }

    if (/^#{2,3} /.test(trimmed)) {
      const level = trimmed.match(/^#+/)![0].length;
      const heading = trimmed.replace(/^#+\s*/, '');
      structure.push({ level, heading });
    }

    if (!trimmed.startsWith('#') && !trimmed.startsWith('>') &&
        !trimmed.startsWith('**') && !trimmed.startsWith('-') &&
        trimmed.length > 100 && excerptCandidates.length < 5) {
      excerptCandidates.push(trimmed);
    }
  }

  const wordCount = content.split(/\s+/).length;
  const excerpt = quotes[0] || excerptCandidates[0]?.substring(0, 297) || '';
  const tags = extractTags(content, category);

  return {
    id: generateId(path.basename(filePath)),
    fileName: path.basename(filePath),
    path: relPath,
    source,
    sourceDir,
    category,
    title: title || path.basename(filePath, '.md'),
    subtitle,
    excerpt,
    wordCount,
    readingTime: Math.ceil(wordCount / 250),
    tags,
    quotes,
    structure,
  };
}

// --- Public API ---

export function loadSynthesisIndex(): ContentDocument[] {
  if (_synthesisIndex) return _synthesisIndex;

  const docs: ContentDocument[] = [];

  for (const { dir } of CORPUS_DIRS) {
    const fullDir = path.join(ROOT, dir);
    if (!fs.existsSync(fullDir)) continue;
    const files = scanDir(fullDir);
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      docs.push(parseDocument(file, content));
    }
  }

  docs.sort((a, b) => a.category.localeCompare(b.category) || a.title.localeCompare(b.title));
  _synthesisIndex = docs;
  return docs;
}

export function loadLibraryIndex(): LibraryDocument[] {
  if (_libraryIndex) return _libraryIndex;

  const docs: LibraryDocument[] = [];

  for (const { dir, label } of CORPUS_DIRS) {
    const fullDir = path.join(ROOT, dir);
    if (!fs.existsSync(fullDir)) continue;

    const scanLib = (dirPath: string, relBase: string) => {
      let entries: fs.Dirent[];
      try { entries = fs.readdirSync(dirPath, { withFileTypes: true }); }
      catch { return; }

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        const relativePath = path.join(relBase, entry.name);

        if (entry.isDirectory()) {
          if (entry.name.startsWith('.') || EXCLUDED_SUBDIRS.has(entry.name)) continue;
          scanLib(fullPath, relativePath);
        } else if (entry.name.endsWith('.md') && entry.name !== 'README.md') {
          try {
            const content = fs.readFileSync(fullPath, 'utf-8');
            const lines = content.split('\n').map(l => l.replace(/\r$/, ''));
            const title = (lines.find(l => l.startsWith('# ')) || '').replace(/^#\s*/, '') || entry.name.replace('.md', '');
            const subtitleLine = lines.find(l => l.startsWith('## '));
            const subtitle = subtitleLine ? subtitleLine.replace(/^##\s*/, '') : '';
            const wordCount = content.split(/\s+/).length;
            const parts = relativePath.split(/[/\\]/);
            const category = parts.length > 2 ? parts[1] : '';

            docs.push({
              title, subtitle, category, wordCount,
              readingTime: Math.ceil(wordCount / 250),
              readPath: '/read/' + relativePath.replace(/\\/g, '/'),
              source: label,
              sourceDir: dir,
            });
          } catch { /* skip unreadable files */ }
        }
      }
    };

    scanLib(fullDir, dir);
  }

  docs.sort((a, b) => a.title.localeCompare(b.title));
  _libraryIndex = docs;
  return docs;
}

export function loadDocumentLinks(): DocumentNodeLinks {
  if (_documentLinks) return _documentLinks;

  const docs = loadSynthesisIndex();
  const constellation = loadConstellation();
  _documentLinks = buildDocumentNodeLinks(docs, constellation);
  return _documentLinks;
}

/** Get all unique content paths for static generation */
export function getAllContentPaths(): { path: string; sourceDir: string }[] {
  const library = loadLibraryIndex();
  return library.map(doc => ({
    path: doc.readPath.replace(/^\/read\//, ''),
    sourceDir: doc.sourceDir,
  }));
}

/** Read raw markdown for a content path */
export function readContent(contentPath: string): string | null {
  const fullPath = path.join(ROOT, contentPath);
  try {
    return fs.readFileSync(fullPath, 'utf-8');
  } catch {
    return null;
  }
}

let _publishedPaths: Set<string> | null = null;

/** Repo-relative paths of every document that has a /read/ route. */
export function getPublishedPaths(): Set<string> {
  if (_publishedPaths) return _publishedPaths;
  _publishedPaths = new Set(getAllContentPaths().map(p => p.path));
  return _publishedPaths;
}

/**
 * Rewrite inter-document links to their /read/ routes.
 *
 * Corpus documents cite each other with paths relative to their own location
 * on disk ("foam-beneath-the-form.md", "../traditions/x.md"). Rendered at
 * /read/<path>/ those resolve to nothing. Targets that exist become links to
 * the published route; targets that don't are left inert rather than made into
 * links that 404 — a document may cite one that is withheld or absent.
 */
export function rewriteDocLinks(html: string, contentPath: string): string {
  const published = getPublishedPaths();
  const baseDir = path.posix.dirname(contentPath.replace(/\\/g, '/'));

  return html.replace(/<a\s+([^>]*?)href="([^"]+)"([^>]*)>/gi, (tag, pre, href: string, post) => {
    if (/^(?:[a-z]+:|#|\/read\/)/i.test(href)) return tag;

    const hashAt = href.indexOf('#');
    const target = hashAt === -1 ? href : href.slice(0, hashAt);
    const anchor = hashAt === -1 ? '' : href.slice(hashAt);
    if (!/\.md$/i.test(target)) return tag;

    const resolved = target.startsWith('/')
      ? path.posix.normalize(target.slice(1))
      : path.posix.normalize(path.posix.join(baseDir, decodeURIComponent(target)));

    if (resolved.startsWith('..') || !published.has(resolved)) {
      return `<a ${pre}class="dead-link" title="Not in the published corpus"${post}>`;
    }
    return `<a ${pre}href="/read/${resolved}${anchor}"${post}>`;
  });
}
