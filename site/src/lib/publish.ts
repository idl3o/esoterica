/**
 * What the library offers outward, and on whose authority.
 */

import fs from 'node:fs';
import path from 'node:path';
import { REPO_ROOT } from './paths';

export const SITE_URL = 'https://esoterica.vercel.app';

/**
 * The library is CC BY 4.0, but that licence is Sam's to grant only over the
 * library's own writing. Some documents are Whisper transcripts of third-party
 * YouTube videos: the words are the speaker's and the recording the
 * publisher's. Those are published in full, with attribution, and marked as
 * what they are — but not under this library's licence, because that is not a
 * licence this library can give.
 *
 * Authorship is decided per document, by the `source: youtube` + `url`
 * frontmatter each transcript carries — not by directory. extractions/ also
 * holds Sam's own harvest syntheses, which are his to licence.
 */
export const LIBRARY_LICENSE = 'CC BY 4.0';
export const THIRD_PARTY_LICENSE = 'rights retained by original speaker/publisher';

export function isThirdParty(contentPath: string): boolean {
  return getAttribution(contentPath) !== null;
}

export function licenseFor(contentPath: string): string {
  return isThirdParty(contentPath) ? THIRD_PARTY_LICENSE : LIBRARY_LICENSE;
}

export interface Attribution {
  url: string;
  title: string;
  channel?: string;
  uploadDate?: string;
}

const _attributions = new Map<string, Attribution | null>();

/**
 * Source metadata for a document transcribed from someone else's recording,
 * read from its own frontmatter. Returns null for the library's own writing,
 * which needs no such notice.
 */
export function getAttribution(contentPath: string): Attribution | null {
  const cached = _attributions.get(contentPath);
  if (cached !== undefined) return cached;

  let result: Attribution | null = null;

  try {
    const raw = fs.readFileSync(path.join(REPO_ROOT, contentPath), 'utf-8');
    const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(raw);
    if (fm) {
      const field = (name: string) =>
        new RegExp(`^${name}:\\s*"?(.*?)"?\\s*$`, 'm').exec(fm[1])?.[1]?.trim() || undefined;
      const url = field('url');
      // A transcript declares both what it came from and where it lives.
      if (url && field('source') === 'youtube') {
        result = {
          url,
          title: field('title') || 'the original recording',
          channel: field('channel'),
          uploadDate: field('upload_date'),
        };
      }
    }
  } catch { /* unreadable, or no frontmatter: the library's own */ }

  _attributions.set(contentPath, result);
  return result;
}
