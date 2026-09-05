/**
 * Link-resolution rulings shared with the harness.
 *
 * `apparatus/scripts/link-rules.json` is the single copy of the alias table,
 * the bare-slug preferences and the directory tie-break order; the Python
 * harness (`linkgraph.py`) and the site renderer (`wikilinks.ts`) both read
 * it, so a ruling changes in one place. A malformed file fails the build
 * loudly, which is intended.
 */

import fs from 'node:fs';
import { repoPath } from './paths';

export interface LinkRules {
  aliases: Record<string, string>;
  prefer: Record<string, string>;
  dir_priority: string[];
}

let _rules: LinkRules | null = null;

export function loadLinkRules(): LinkRules {
  if (_rules) return _rules;
  const raw = fs.readFileSync(repoPath('apparatus', 'scripts', 'link-rules.json'), 'utf-8');
  const parsed = JSON.parse(raw) as Partial<LinkRules>;
  _rules = {
    aliases: parsed.aliases ?? {},
    prefer: parsed.prefer ?? {},
    dir_priority: parsed.dir_priority ?? [],
  };
  return _rules;
}
