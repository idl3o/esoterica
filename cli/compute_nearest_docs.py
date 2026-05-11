#!/usr/bin/env python3
"""
compute_nearest_docs.py — For each worklist node, find the top-5 existing
synthesis docs by tag-overlap with the node's essence + connections.

Reads:  cli/output/empty-powerful-nodes.json
Writes: cli/output/sweep-nearest-docs.json

Used by emit_briefs.py to give each author-agent a list of style exemplars
and verified cross-reference paths.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TERM_PATTERNS = [
    "consciousness", "awareness", "recognition", "polarity", "density",
    "wanderer", "service", "manifestation", "timeline", "synchronicity",
    "archetype", "apollo", "mercury", "kalki", "samael",
    "singularity", "galactic", "cosmic", "source", "unity",
    "sacred geometry", "fibonacci", "reality programming",
    "love-light", "frequency", "resonance", "vibration",
    "enlightenment", "awakening", "breakthrough", "integration",
]

DIRS = ["synthesis", "translated", "fiction-bridges", "distillations",
        "protocols", "seeds", "traditions", "extractions",
        "correspondences", "journey", "garden", "harvest",
        "world-tree", "memory-palace"]


def main():
    print("[1/3] scanning markdown corpus…", file=sys.stderr)
    docs = []
    for d in DIRS:
        full = ROOT / d
        if not full.exists():
            continue
        for dirpath, dirnames, fns in os.walk(full):
            dirnames[:] = [x for x in dirnames if not x.startswith('.')]
            for fn in fns:
                if not fn.endswith('.md'):
                    continue
                p = Path(dirpath) / fn
                try:
                    text = p.read_text(encoding='utf-8', errors='replace').lower()
                except Exception:
                    continue
                tags = set(t for t in TERM_PATTERNS if t in text)
                # title (first H1, frontmatter-aware)
                title = ''
                with open(p, encoding='utf-8', errors='replace') as fh:
                    in_fm = False
                    past_fm = False
                    for line in fh:
                        s = line.strip()
                        if s == '---':
                            if not past_fm and not in_fm:
                                in_fm = True
                                continue
                            if in_fm:
                                in_fm = False
                                past_fm = True
                                continue
                        if in_fm:
                            continue
                        if s.startswith('# '):
                            title = s[2:].strip()
                            break
                docs.append({
                    'path': str(p.relative_to(ROOT)),
                    'title': title or p.stem,
                    'tags': tags,
                })
    print(f"      {len(docs)} docs indexed", file=sys.stderr)

    print("[2/3] loading worklist…", file=sys.stderr)
    work = json.loads((ROOT / 'cli' / 'output' / 'empty-powerful-nodes.json').read_text())
    print(f"      {len(work)} worklist entries", file=sys.stderr)

    print("[3/3] computing tag-overlap…", file=sys.stderr)
    near = {}
    for w in work:
        interests = set()
        srcs = [w.get('essence', ''), w.get('id', '')] + w.get('connections', [])
        for src in srcs:
            s = (src or '').replace('_', ' ').lower()
            for term in TERM_PATTERNS:
                if term in s:
                    interests.add(term)
        if not interests:
            desc = (w.get('description', '') or '').lower()
            for term in TERM_PATTERNS:
                if term in desc:
                    interests.add(term)
        scored = []
        for d in docs:
            overlap = len(d['tags'] & interests)
            if overlap > 0:
                scored.append((overlap, d['path'], d['title']))
        scored.sort(reverse=True)
        near[w['id']] = [{'path': p, 'title': t, 'overlap': o} for o, p, t in scored[:5]]

    out = ROOT / 'cli' / 'output' / 'sweep-nearest-docs.json'
    out.write_text(json.dumps(near, indent=2))
    print(f"      → {out.relative_to(ROOT)}", file=sys.stderr)


if __name__ == '__main__':
    main()
