/**
 * Meta-Zeitgeist indexer.
 * Extracts items from zeitgeist readings and tracks persistence across timescales.
 */

import { loadZeitgeist, type ZeitgeistReading } from './zeitgeist';
import fs from 'node:fs';
import path from 'node:path';

// Types
export type Timescale = 'SURFACE' | 'CURRENT' | 'DEEP' | 'TECTONIC';

export interface ItemAppearance {
  date: string;
  timescale: Timescale;
  title: string;
  description: string;
  gap: string | null;
}

export interface ZeitgeistItem {
  id: string;
  title: string;
  timescale: Timescale;

  appearances: ItemAppearance[];

  firstSeen: string;
  lastSeen: string;
  appearanceCount: number;
  daysPersisted: number;

  titleVariants: string[];
  status: 'active' | 'metabolised' | 'dormant';

  latestDescription: string;
  latestGap: string | null;
}

export interface Correspondence {
  date: string;
  pattern: string;
  summary: string;
}

export interface ReadingSummary {
  date: string;
  displayDate: string;
  correspondence: string | null;
  edge: string | null;
  itemCount: {
    surface: number;
    current: number;
    deep: number;
    tectonic: number;
  };
}

export interface ZeitgeistItemsIndex {
  meta: {
    generated: string;
    readingsCount: number;
    dateRange: { first: string; last: string };
  };
  items: ZeitgeistItem[];
  correspondences: Correspondence[];
  readings: ReadingSummary[];
  allDates: string[];
}

// Curation file for manual merges
interface CurationEntry {
  canonical: string;
  canonicalTitle: string;
  variants: string[];
}

interface CurationFile {
  merges: CurationEntry[];
  timescaleOverrides?: Record<string, Timescale>;
}

let _curationCache: CurationFile | null = null;

function loadCuration(): CurationFile {
  if (_curationCache) return _curationCache;

  try {
    const curationPath = path.join(process.cwd(), 'src', 'data', 'zeitgeist-items-curation.json');
    const content = fs.readFileSync(curationPath, 'utf-8');
    _curationCache = JSON.parse(content);
    return _curationCache!;
  } catch {
    // Return empty curation if file doesn't exist
    return { merges: [] };
  }
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 60);
}

function parseSection(markdown: string, sectionName: string): string | null {
  // Match section header followed by italic description, then content until next section
  const regex = new RegExp(
    `## ${sectionName}\\s*\\n\\*[^*]+\\*\\s*\\n([\\s\\S]*?)(?=\\n## |$)`,
    'i'
  );
  const match = markdown.match(regex);
  return match ? match[1].trim() : null;
}

function extractItems(sectionContent: string, timescale: Timescale): { title: string; description: string; gap: string | null }[] {
  const items: { title: string; description: string; gap: string | null }[] = [];

  // Match bold title followed by content until next bold title or end
  // Pattern: **Title.** or **Title:** followed by description
  const itemRegex = /\*\*([^*]+?)[.:]?\*\*\.?\s*([\s\S]*?)(?=\n\n\*\*[^*]+\*\*|$)/g;

  let match;
  while ((match = itemRegex.exec(sectionContent)) !== null) {
    const title = match[1].trim();
    let description = match[2].trim();

    // Extract gap (final italicised text)
    let gap: string | null = null;
    const gapMatch = description.match(/\*([^*]+)\*\s*$/);
    if (gapMatch) {
      gap = gapMatch[1].trim();
      // Remove gap from description
      description = description.replace(/\*([^*]+)\*\s*$/, '').trim();
    }

    // Skip if title is too short or looks like a subheading
    if (title.length < 5) continue;

    items.push({ title, description, gap });
  }

  return items;
}

function extractCorrespondence(markdown: string): { pattern: string; summary: string } | null {
  const section = parseSection(markdown, 'CORRESPONDENCE');
  if (!section) return null;

  // Look for "The pattern is **X**" or "pattern: **X**" or just first bold text
  const patternMatch = section.match(/(?:The pattern(?:\s+operating[^*]*)?\s+is\s+\*\*([^*]+)\*\*|\*\*([^*]+)\*\*)/i);
  const pattern = patternMatch ? (patternMatch[1] || patternMatch[2]).trim() : 'Unknown pattern';

  // Get first paragraph as summary
  const firstPara = section.split('\n\n')[0];
  const summary = firstPara.replace(/\*\*/g, '').substring(0, 300);

  return { pattern, summary };
}

function extractEdge(markdown: string): string | null {
  const stateSection = parseSection(markdown, 'STATE');
  if (!stateSection) return null;

  const edgeMatch = stateSection.match(/\*\*THE EDGE[:\s]*\*\*:?\s*([\s\S]*?)(?:\n\n---|\n\nSources:|$)/i);
  if (edgeMatch) {
    return edgeMatch[1].trim().substring(0, 400);
  }
  return null;
}

function findCanonicalId(title: string, curation: CurationFile): { id: string; canonicalTitle: string } | null {
  const slug = slugify(title);

  for (const merge of curation.merges) {
    if (merge.canonical === slug || merge.variants.includes(slug)) {
      return { id: merge.canonical, canonicalTitle: merge.canonicalTitle };
    }
    // Also check if title text matches
    if (title.toLowerCase().includes(merge.canonicalTitle.toLowerCase()) ||
        merge.variants.some(v => title.toLowerCase().includes(v.replace(/-/g, ' ')))) {
      return { id: merge.canonical, canonicalTitle: merge.canonicalTitle };
    }
  }

  return null;
}

function calculateDaysPersisted(firstSeen: string, lastSeen: string): number {
  const first = new Date(firstSeen);
  const last = new Date(lastSeen);
  return Math.round((last.getTime() - first.getTime()) / (1000 * 60 * 60 * 24));
}

function determineStatus(item: ZeitgeistItem, allDates: string[]): 'active' | 'metabolised' | 'dormant' {
  if (allDates.length === 0) return 'active';

  const latestReadingDate = allDates[0]; // Dates are sorted newest first
  const daysSinceLastSeen = calculateDaysPersisted(item.lastSeen, latestReadingDate);

  // Active: appeared in last 3 days
  if (daysSinceLastSeen <= 3) return 'active';

  // Dormant: hasn't appeared in > 7 days but was seen multiple times
  if (daysSinceLastSeen > 7 && item.appearanceCount > 1) return 'dormant';

  // Metabolised: single appearance, now gone
  if (item.appearanceCount === 1 && daysSinceLastSeen > 3) return 'metabolised';

  return 'dormant';
}

let _indexCache: ZeitgeistItemsIndex | null = null;

export function loadZeitgeistItems(): ZeitgeistItemsIndex {
  if (_indexCache) return _indexCache;

  const readings = loadZeitgeist();
  const curation = loadCuration();

  const itemsMap = new Map<string, ZeitgeistItem>();
  const correspondences: Correspondence[] = [];
  const readingSummaries: ReadingSummary[] = [];
  const allDates = readings.map(r => r.date);

  // Process each reading (they come newest first, we want oldest first for processing)
  const sortedReadings = [...readings].reverse();

  for (const reading of sortedReadings) {
    const itemCount = { surface: 0, current: 0, deep: 0, tectonic: 0 };

    // Extract items from each timescale section
    const timescales: Timescale[] = ['SURFACE', 'CURRENT', 'DEEP', 'TECTONIC'];

    for (const timescale of timescales) {
      const sectionContent = parseSection(reading.zeitMarkdown, timescale);
      if (!sectionContent) continue;

      const extractedItems = extractItems(sectionContent, timescale);
      itemCount[timescale.toLowerCase() as keyof typeof itemCount] = extractedItems.length;

      for (const extracted of extractedItems) {
        // Check curation for canonical ID
        const canonical = findCanonicalId(extracted.title, curation);
        const id = canonical?.id || slugify(extracted.title);
        const canonicalTitle = canonical?.canonicalTitle || extracted.title;

        const appearance: ItemAppearance = {
          date: reading.date,
          timescale,
          title: extracted.title,
          description: extracted.description,
          gap: extracted.gap,
        };

        if (itemsMap.has(id)) {
          // Update existing item
          const existing = itemsMap.get(id)!;
          existing.appearances.push(appearance);
          existing.lastSeen = reading.date;
          existing.appearanceCount++;
          existing.latestDescription = extracted.description;
          existing.latestGap = extracted.gap;
          existing.timescale = timescale; // Update to most recent timescale
          if (!existing.titleVariants.includes(extracted.title)) {
            existing.titleVariants.push(extracted.title);
          }
        } else {
          // Create new item
          const newItem: ZeitgeistItem = {
            id,
            title: canonicalTitle,
            timescale,
            appearances: [appearance],
            firstSeen: reading.date,
            lastSeen: reading.date,
            appearanceCount: 1,
            daysPersisted: 0,
            titleVariants: [extracted.title],
            status: 'active',
            latestDescription: extracted.description,
            latestGap: extracted.gap,
          };
          itemsMap.set(id, newItem);
        }
      }
    }

    // Extract correspondence
    const corr = extractCorrespondence(reading.zeitMarkdown);
    if (corr) {
      correspondences.push({
        date: reading.date,
        pattern: corr.pattern,
        summary: corr.summary,
      });
    }

    // Extract edge
    const edge = extractEdge(reading.zeitMarkdown);

    readingSummaries.push({
      date: reading.date,
      displayDate: reading.displayDate,
      correspondence: corr?.pattern || null,
      edge,
      itemCount,
    });
  }

  // Post-process items
  const items = Array.from(itemsMap.values());
  for (const item of items) {
    item.daysPersisted = calculateDaysPersisted(item.firstSeen, item.lastSeen);
    item.status = determineStatus(item, allDates);
  }

  // Sort items by appearance count (most persistent first)
  items.sort((a, b) => b.appearanceCount - a.appearanceCount);

  // Reverse readings to be newest first for display
  readingSummaries.reverse();
  correspondences.reverse();

  const index: ZeitgeistItemsIndex = {
    meta: {
      generated: new Date().toISOString(),
      readingsCount: readings.length,
      dateRange: {
        first: sortedReadings[0]?.date || '',
        last: sortedReadings[sortedReadings.length - 1]?.date || '',
      },
    },
    items,
    correspondences,
    readings: readingSummaries,
    allDates,
  };

  _indexCache = index;
  return index;
}

// Helper functions for views

export function getItemsByTimescale(timescale: Timescale): ZeitgeistItem[] {
  const index = loadZeitgeistItems();
  return index.items
    .filter(item => item.timescale === timescale)
    .sort((a, b) => b.appearanceCount - a.appearanceCount);
}

export function getItemById(id: string): ZeitgeistItem | null {
  const index = loadZeitgeistItems();
  return index.items.find(item => item.id === id) || null;
}

export function getStats(): {
  total: number;
  active: number;
  metabolised: number;
  dormant: number;
  avgPersistence: number;
  byTimescale: Record<Timescale, number>;
} {
  const index = loadZeitgeistItems();
  const items = index.items;

  const byStatus = {
    active: items.filter(i => i.status === 'active').length,
    metabolised: items.filter(i => i.status === 'metabolised').length,
    dormant: items.filter(i => i.status === 'dormant').length,
  };

  const byTimescale: Record<Timescale, number> = {
    SURFACE: items.filter(i => i.timescale === 'SURFACE').length,
    CURRENT: items.filter(i => i.timescale === 'CURRENT').length,
    DEEP: items.filter(i => i.timescale === 'DEEP').length,
    TECTONIC: items.filter(i => i.timescale === 'TECTONIC').length,
  };

  const totalPersistence = items.reduce((sum, i) => sum + i.daysPersisted, 0);
  const avgPersistence = items.length > 0 ? Math.round(totalPersistence / items.length) : 0;

  return {
    total: items.length,
    ...byStatus,
    avgPersistence,
    byTimescale,
  };
}

export function getAppearanceMap(itemId: string, allDates: string[]): boolean[] {
  const item = getItemById(itemId);
  if (!item) return allDates.map(() => false);

  const appearanceDates = new Set(item.appearances.map(a => a.date));
  return allDates.map(date => appearanceDates.has(date));
}
