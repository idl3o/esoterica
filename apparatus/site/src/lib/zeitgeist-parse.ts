/**
 * Pure parsers for zeitgeist readings: markdown in, data out, no I/O.
 *
 * The reading template has drifted across the archive (seven spellings of
 * THE EDGE, bold and unbold correspondence patterns, descriptor lines with and
 * without a blank line above them, bulleted and unbulleted items). These
 * parsers accept every variant the archive contains, and
 * `zeitgeist-parse.test.ts` runs them over the whole archive, so a new variant
 * fails a test rather than silently blanking a card on the live site.
 *
 * Decisions, not accidents — do not undo:
 * - Item titles are extracted exactly as before. Item ids are slugified
 *   titles and are public URLs (/zeitgeist/meta/item/<id>).
 * - Section content is stripped of its trailing `---` rule. Left in, the rule
 *   sits after the last item's italic gap and the end-anchored gap regex
 *   misses it: every section of every reading lost its final gap that way.
 */

export const TIMESCALES = ['SURFACE', 'CURRENT', 'DEEP', 'TECTONIC'] as const;
export type Timescale = (typeof TIMESCALES)[number];

export interface ParsedItem {
  readonly title: string;
  readonly description: string;
  readonly gap: string | null;
}

export interface ParsedCorrespondence {
  readonly pattern: string;
  readonly summary: string;
}

const EDGE_MAX = 400;
const SUMMARY_MAX = 250;
const CORRESPONDENCE_SUMMARY_MAX = 300;
const PATTERN_FALLBACK_MAX = 160;
const MIN_TITLE_LENGTH = 5;

/** Working copies on Windows arrive CRLF; every regex below assumes LF. */
export function normaliseNewlines(markdown: string): string {
  return markdown.replace(/\r\n/g, '\n');
}

function stripEmphasis(text: string): string {
  return text.replace(/\*\*/g, '').replace(/\*/g, '');
}

/** Drop the Sources block and any trailing horizontal rule from a section. */
function stripTail(content: string): string {
  return content
    .replace(/\n(?:-{3,}[ \t]*\n+)?Sources:[\s\S]*$/, '')
    .replace(/\n+-{3,}\s*$/, '')
    .trim();
}

/**
 * Content of a `## NAME` section, without its italic descriptor line, its
 * trailing rule, or the Sources block. The descriptor is optional and may be
 * separated from the heading by a blank line (the February 2026 template) or
 * not (every template since).
 */
export function parseSection(markdown: string, sectionName: string): string | null {
  const regex = new RegExp(
    `(?:^|\\n)## ${sectionName}[^\\n]*\\n+(?:\\*[^*\\n]+\\*[ \\t]*\\n)?([\\s\\S]*?)(?=\\n## |$)`,
    'i',
  );
  const match = regex.exec(normaliseNewlines(markdown));
  const content = match?.[1];
  if (content === undefined) return null;
  const stripped = stripTail(content);
  return stripped === '' ? null : stripped;
}

/**
 * Items of a timescale section: a bold title opening a paragraph (optionally
 * as a `- ` bullet), then everything up to the next such title. The gap is the
 * item's closing italic passage, where it has one.
 */
export function extractItems(sectionContent: string): ParsedItem[] {
  const items: ParsedItem[] = [];
  const itemRegex = /\*\*([^*]+?)[.:]?\*\*\.?\s*([\s\S]*?)(?=\n\n(?:- )?\*\*[^*]+\*\*|$)/g;

  for (const match of sectionContent.matchAll(itemRegex)) {
    const title = (match[1] ?? '').trim();
    if (title.length < MIN_TITLE_LENGTH) continue;

    const body = (match[2] ?? '').trim();
    const gapMatch = /\*([^*]+)\*\s*$/.exec(body);
    const gap = gapMatch?.[1]?.trim() ?? null;
    const description = gapMatch ? body.slice(0, gapMatch.index).trim() : body;

    items.push({ title, description, gap });
  }

  return items;
}

/** First bold phrase after the DEEP (or legacy DEPTH) heading. */
export function extractHeadline(markdown: string): string {
  const md = normaliseNewlines(markdown);
  const match = /## DEEP[\s\S]*?\*\*([^*]+)\*\*/.exec(md) ?? /## DEPTH[\s\S]*?\*\*([^*]+)\*\*/.exec(md);
  return match?.[1] ?? '';
}

/** Opening paragraph of STATE, emphasis stripped, for archive cards. */
export function extractSummary(markdown: string): string {
  const state = parseSection(markdown, 'STATE');
  if (state === null) return '';
  const firstPara = state.split('\n\n')[0] ?? '';
  const text = stripEmphasis(firstPara).trim();
  return text === '' ? '' : `${text.substring(0, SUMMARY_MAX)}...`;
}

function firstSentence(text: string, max: number): string {
  const flat = stripEmphasis(text).replace(/\s+/g, ' ').trim();
  const end = flat.search(/[.!?](?:\s|$)/);
  const sentence = end === -1 ? flat : flat.slice(0, end + 1);
  if (sentence.length <= max) return sentence;
  const cut = sentence.slice(0, max);
  const lastSpace = cut.lastIndexOf(' ');
  return `${lastSpace > 0 ? cut.slice(0, lastSpace) : cut}…`;
}

/**
 * The correspondence pattern: "The pattern is **X**", else the section's first
 * bold phrase, else its first sentence. Readings written without any bold in
 * the section used to index as "Unknown pattern".
 */
export function extractCorrespondence(markdown: string): ParsedCorrespondence | null {
  const section = parseSection(markdown, 'CORRESPONDENCE');
  if (section === null) return null;

  const match = /(?:The pattern(?:\s+operating[^*]*)?\s+is\s+\*\*([^*]+)\*\*|\*\*([^*]+)\*\*)/i.exec(section);
  const bold = (match?.[1] ?? match?.[2])?.trim();
  const pattern = bold !== undefined && bold !== '' ? bold : firstSentence(section, PATTERN_FALLBACK_MAX);

  const firstPara = section.split('\n\n')[0] ?? '';
  const summary = firstPara.replace(/\*\*/g, '').substring(0, CORRESPONDENCE_SUMMARY_MAX);

  return { pattern, summary };
}

/**
 * THE EDGE, in any spelling the archive has used: bold or plain, closed by a
 * full stop, a colon (inside or outside the bold), a dash or nothing, on the
 * same line as its text or on the line above. Plain spellings must be upper case and
 * open a line, so prose that mentions "the edge" is not mistaken for it.
 */
export function extractEdge(markdown: string): string | null {
  const state = parseSection(markdown, 'STATE');
  if (state === null) return null;

  const match = /(?:^|\n)[ \t]*(?:#{1,6}[ \t]+)?\*{0,2}THE EDGE[.:]?\*{0,2}[.:]?[ \t]*(?:[—–-][ \t]*)?\n*\s*([\s\S]+)$/.exec(state);
  const text = match?.[1]?.trim();
  return text === undefined || text === '' ? null : text.substring(0, EDGE_MAX);
}
