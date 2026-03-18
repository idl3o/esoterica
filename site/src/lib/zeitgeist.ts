/**
 * Zeitgeist file parser.
 * Loads and parses zeitgeist readings from synthesis/zeitgeist/.
 */

import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';
import { repoPath } from './paths';

export interface ZeitgeistReading {
  date: string;
  displayDate: string;
  headline: string;
  summary: string;
  hasGeist: boolean;
  isIntegrated: boolean;
  zeitHtml: string;
  geistHtml: string | null;
  zeitMarkdown: string;
}

let _cached: ZeitgeistReading[] | null = null;

export function loadZeitgeist(): ZeitgeistReading[] {
  if (_cached) return _cached;

  const zeitgeistDir = repoPath('synthesis', 'zeitgeist');

  let files: string[];
  try {
    files = fs.readdirSync(zeitgeistDir);
  } catch {
    return [];
  }

  // Collect dates, new format takes priority
  const dateMap = new Map<string, { type: 'paired' | 'integrated'; file: string }>();

  for (const f of files) {
    const pairedMatch = f.match(/^zeit-(\d{4}-\d{2}-\d{2})\.md$/);
    if (pairedMatch) {
      dateMap.set(pairedMatch[1], { type: 'paired', file: f });
    }
  }

  for (const f of files) {
    const integratedMatch = f.match(/^zeitgeist-(\d{4}-\d{2}-\d{2})\.md$/);
    if (integratedMatch) {
      dateMap.set(integratedMatch[1], { type: 'integrated', file: f });
    }
  }

  const sortedDates = Array.from(dateMap.keys()).sort().reverse();
  const archive: ZeitgeistReading[] = [];

  for (const date of sortedDates) {
    const entry = dateMap.get(date)!;

    if (entry.type === 'integrated') {
      const markdown = fs.readFileSync(path.join(zeitgeistDir, entry.file), 'utf-8');
      const html = marked.parse(markdown) as string;

      const deepMatch = markdown.match(/## DEEP[\s\S]*?\*\*([^*]+)\*\*/);
      const depthMatch = markdown.match(/## DEPTH[\s\S]*?\*\*([^*]+)\*\*/);
      const headline = deepMatch?.[1] || depthMatch?.[1] || '';

      const stateMatch = markdown.match(/## STATE[\s\S]*?\r?\n\r?\n\*[^*]+\*\r?\n\r?\n([\s\S]*?)(?:\r?\n\r?\n|$)/);
      const summary = stateMatch
        ? stateMatch[1].replace(/\*\*/g, '').replace(/\*/g, '').substring(0, 250) + '...'
        : '';

      const dateObj = new Date(date + 'T00:00:00');
      const displayDate = dateObj.toLocaleDateString('en-GB', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
      });

      archive.push({
        date, displayDate, headline, summary,
        hasGeist: false, isIntegrated: true,
        zeitHtml: html, geistHtml: null, zeitMarkdown: markdown
      });
    } else {
      const zeitPath = path.join(zeitgeistDir, entry.file);
      const zeitMarkdown = fs.readFileSync(zeitPath, 'utf-8');
      const zeitHtml = marked.parse(zeitMarkdown) as string;

      const depthMatch = zeitMarkdown.match(/## DEPTH[\s\S]*?\*\*([^*]+)\*\*/);
      const headline = depthMatch?.[1] || '';

      const stateMatch = zeitMarkdown.match(/## STATE[\s\S]*?\r?\n\r?\n\*[^*]+\*\r?\n\r?\n([\s\S]*?)(?:\r?\n\r?\n|$)/);
      const summary = stateMatch
        ? stateMatch[1].replace(/\*\*/g, '').replace(/\*/g, '').substring(0, 250) + '...'
        : '';

      const geistFile = `geist-${date}.md`;
      let geistHtml: string | null = null;
      let hasGeist = false;
      try {
        const geistMarkdown = fs.readFileSync(path.join(zeitgeistDir, geistFile), 'utf-8');
        geistHtml = marked.parse(geistMarkdown) as string;
        hasGeist = true;
      } catch { /* geist may not exist */ }

      const dateObj = new Date(date + 'T00:00:00');
      const displayDate = dateObj.toLocaleDateString('en-GB', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
      });

      archive.push({
        date, displayDate, headline, summary,
        hasGeist, isIntegrated: false,
        zeitHtml, geistHtml, zeitMarkdown
      });
    }
  }

  _cached = archive;
  return archive;
}

export function getLatestZeitgeist(): ZeitgeistReading | null {
  const archive = loadZeitgeist();
  return archive[0] || null;
}
