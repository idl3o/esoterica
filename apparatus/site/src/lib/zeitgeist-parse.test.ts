import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { corpusPath } from './paths';
import {
  TIMESCALES,
  extractCorrespondence,
  extractEdge,
  extractHeadline,
  extractItems,
  extractSummary,
  normaliseNewlines,
  parseSection,
} from './zeitgeist-parse';

const reading = (state: string, correspondence = 'The week turns on **one hinge**. More follows.') => `# ZEITGEIST — 1 January 2026

*A reading of the present moment.*

---

## SURFACE
*Events that metabolise in days.*

**First thing happened.** It happened on Tuesday. *The gap of the first.*

**Second thing:** It followed. *The gap of the second, which is last in its section.*

---

## DEEP
*Phase transitions that metabolise in years.*

**The deep headline.** First paragraph.

A continuation paragraph with **inline bold** that is not a title.

---

## CORRESPONDENCE
*The same pattern at every scale.*

${correspondence}

## STATE
*The reading.*

Metta-darshan *first*. The **opening** paragraph.

Then lila.

${state}

---

Sources:
- https://example.org/a

*Channel note: a closing italic paragraph that is not the summary.*
`;

describe('parseSection', () => {
  it('drops the descriptor, the trailing rule and the Sources block', () => {
    const surface = parseSection(reading('**THE EDGE:** x'), 'SURFACE');
    expect(surface?.startsWith('**First thing happened.**')).toBe(true);
    expect(surface?.endsWith('last in its section.*')).toBe(true);

    const state = parseSection(reading('**THE EDGE:** the edge text'), 'STATE');
    expect(state).not.toContain('Sources:');
    expect(state).not.toContain('example.org');
    expect(state?.endsWith('the edge text')).toBe(true);
  });

  it('accepts a blank line between heading and descriptor (February 2026 template)', () => {
    const md = '## SURFACE\n\n*Events that metabolise in days.*\n\n- **A bulleted item**, with text.\n\n---\n\n## CURRENT\n*x*\n\n**B.** y';
    expect(parseSection(md, 'SURFACE')).toBe('- **A bulleted item**, with text.');
  });

  it('accepts a section with no descriptor at all', () => {
    expect(parseSection('## DEEP\n\n**Headline.** Body.', 'DEEP')).toBe('**Headline.** Body.');
  });

  it('is indifferent to CRLF working copies', () => {
    const lf = reading('**THE EDGE:** x');
    const crlf = lf.replace(/\n/g, '\r\n');
    expect(normaliseNewlines(crlf)).toBe(lf);
    for (const name of [...TIMESCALES, 'CORRESPONDENCE', 'STATE']) {
      expect(parseSection(crlf, name)).toBe(parseSection(lf, name));
    }
  });

  it('returns null for an absent section', () => {
    expect(parseSection('## SURFACE\n*x*\n\n**Abcdef.** y', 'TECTONIC')).toBeNull();
  });
});

describe('extractItems', () => {
  it('keeps the gap of the last item in a section', () => {
    const items = extractItems(parseSection(reading('**THE EDGE:** x'), 'SURFACE') ?? '');
    expect(items.map(i => i.title)).toEqual(['First thing happened', 'Second thing']);
    expect(items.map(i => i.gap)).toEqual(['The gap of the first.', 'The gap of the second, which is last in its section.']);
    expect(items[1]?.description).toBe('It followed.');
  });

  it('treats continuation paragraphs and inline bold as body, not as items', () => {
    const items = extractItems(parseSection(reading('**THE EDGE:** x'), 'DEEP') ?? '');
    expect(items).toHaveLength(1);
    expect(items[0]?.title).toBe('The deep headline');
    expect(items[0]?.description).toContain('inline bold');
    expect(items[0]?.gap).toBeNull();
  });

  it('splits bulleted items', () => {
    const items = extractItems('- **One thing happened**, and then.\n\n- **Another thing.** More.\n\n- **A third thing**: last.');
    expect(items.map(i => i.title)).toEqual(['One thing happened', 'Another thing', 'A third thing']);
    expect(items[0]?.description).toBe(', and then.');
  });

  it('skips titles too short to be items', () => {
    expect(extractItems('**No.** Body.\n\n**A real title.** Body.').map(i => i.title)).toEqual(['A real title']);
  });
});

describe('extractEdge', () => {
  const spellings = [
    '**THE EDGE**',
    '**THE EDGE**:',
    '**THE EDGE.**',
    '**THE EDGE:**',
    'THE EDGE',
    'THE EDGE.',
    'THE EDGE:',
  ];

  it.each(spellings)('reads the spelling %s', spelling => {
    expect(extractEdge(reading(`${spelling} What presses against the moment.`))).toBe('What presses against the moment.');
  });

  it('reads an edge whose text starts on the next paragraph', () => {
    expect(extractEdge(reading('**THE EDGE**\n\nWhat presses.'))).toBe('What presses.');
  });

  it('drops a dash between the marker and its text (June 2026)', () => {
    expect(extractEdge(reading('**THE EDGE** — what is pressing.'))).toBe('what is pressing.');
  });

  it('does not mistake prose for the marker', () => {
    expect(extractEdge(reading('Something sits at the edge of the week.'))).toBeNull();
  });

  it('caps the edge at 400 characters', () => {
    expect(extractEdge(reading(`**THE EDGE:** ${'x'.repeat(900)}`))).toHaveLength(400);
  });
});

describe('extractCorrespondence', () => {
  it('reads "The pattern is **X**"', () => {
    const c = extractCorrespondence(reading('**THE EDGE:** x', 'Across every scale. The pattern is **the hinge**.'));
    expect(c?.pattern).toBe('the hinge');
  });

  it('takes whichever bold phrase comes first (shipped behaviour, kept so past labels do not move)', () => {
    const c = extractCorrespondence(reading('**THE EDGE:** x', 'A **stray** phrase first. The pattern is **the hinge**.'));
    expect(c?.pattern).toBe('stray');
  });

  it('takes the first bold phrase', () => {
    expect(extractCorrespondence(reading('**THE EDGE:** x'))?.pattern).toBe('one hinge');
  });

  it('falls back to the first sentence when the section has no bold', () => {
    const c = extractCorrespondence(reading('**THE EDGE:** x', 'The week turns on exit, not voice. A second sentence.'));
    expect(c?.pattern).toBe('The week turns on exit, not voice.');
    expect(c?.summary).toBe('The week turns on exit, not voice. A second sentence.');
  });

  it('truncates a long fallback at a word boundary', () => {
    const long = `${'word '.repeat(60)}end.`;
    const pattern = extractCorrespondence(reading('**THE EDGE:** x', long))?.pattern ?? '';
    expect(pattern.length).toBeLessThanOrEqual(161);
    expect(pattern.endsWith('…')).toBe(true);
    expect(pattern).not.toMatch(/wor…$/);
  });
});

describe('extractHeadline and extractSummary', () => {
  it('reads the first bold phrase of DEEP', () => {
    expect(extractHeadline(reading('**THE EDGE:** x'))).toBe('The deep headline.');
  });

  it('falls back to the legacy DEPTH heading', () => {
    expect(extractHeadline('## DEPTH\n\n**Old headline.** Body.')).toBe('Old headline.');
  });

  it('summarises the opening STATE paragraph without emphasis marks', () => {
    expect(extractSummary(reading('**THE EDGE:** x'))).toBe('Metta-darshan first. The opening paragraph....');
  });

  it('is empty when there is no STATE section', () => {
    expect(extractSummary('## DEEP\n\n**H.** b')).toBe('');
  });
});

/**
 * The archive is the fixture. Every integrated reading must yield what the
 * site renders from it; a reading that does not is a template variant the
 * parsers have not met, and the fix belongs here before it reaches the site.
 */
describe('the archive', () => {
  const dir = corpusPath('synthesis', 'zeitgeist');
  const files = fs
    .readdirSync(dir)
    .filter(f => /^zeitgeist-\d{4}-\d{2}-\d{2}\.md$/.test(f))
    .sort();
  const load = (f: string) => fs.readFileSync(path.join(dir, f), 'utf-8');

  it('is found', () => {
    expect(files.length).toBeGreaterThanOrEqual(35);
  });

  it.each(files)('%s yields a headline, a summary, a pattern and an edge', f => {
    const md = load(f);
    expect(extractHeadline(md), 'headline').not.toBe('');
    expect(extractSummary(md), 'summary').not.toBe('');
    expect(extractCorrespondence(md)?.pattern ?? '', 'pattern').not.toBe('');
    expect(extractEdge(md), 'edge').not.toBeNull();
  });

  it.each(files)('%s has items in all four timescales', f => {
    const md = load(f);
    for (const timescale of TIMESCALES) {
      const section = parseSection(md, timescale);
      expect(section, timescale).not.toBeNull();
      expect(extractItems(section ?? '').length, `${timescale} items`).toBeGreaterThan(0);
    }
  });

  it.each(files)('%s gives every SURFACE and CURRENT item that ends in italics its gap', f => {
    const md = load(f);
    for (const timescale of ['SURFACE', 'CURRENT'] as const) {
      const items = extractItems(parseSection(md, timescale) ?? '');
      const last = items.at(-1);
      expect(last?.description ?? '', `${timescale} last description`).not.toMatch(/-{3,}\s*$/);
    }
  });

  /**
   * Item ids are slugified titles and are public URLs. The legacy regex below
   * is the one the site shipped with; nothing it found may go missing.
   */
  it.each(files)('%s loses no item title the legacy parser found', f => {
    const md = normaliseNewlines(load(f));
    for (const timescale of TIMESCALES) {
      const legacySection = new RegExp(`## ${timescale}\\s*\\n\\*[^*]+\\*\\s*\\n([\\s\\S]*?)(?=\\n## |$)`, 'i').exec(md)?.[1]?.trim() ?? '';
      const legacyTitles = [...legacySection.matchAll(/\*\*([^*]+?)[.:]?\*\*\.?\s*([\s\S]*?)(?=\n\n\*\*[^*]+\*\*|$)/g)]
        .map(m => (m[1] ?? '').trim())
        .filter(t => t.length >= 5);
      const titles = new Set(extractItems(parseSection(md, timescale) ?? '').map(i => i.title));
      for (const title of legacyTitles) expect(titles, `${timescale}: ${title}`).toContain(title);
    }
  });
});
