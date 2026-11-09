"""Copyright sweep: find where the corpus reproduces other people's text at length.

Mechanical signals only; every hit needs a human reading. Per markdown file:
  blockquote runs      contiguous '>' lines, words per run
  epigraphs            italic quoted lines (*"..."*) and their attribution
  long quoted spans    text inside one pair of quotation marks, 40 words or more
  keyword flags        lyrics, transcript, translated by, (c), all rights reserved
  attributions         '-- Name, Work' lines, aggregated corpus-wide

Usage: python apparatus/scripts/copyright_sweep.py [--json OUT] [--min-words N] [--top N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Curly quotes have distinct open and close marks, so a regex pairs them correctly.
# Straight quotes do not: a regex would bridge from one quotation's close to the
# next one's open, so those are paired by position in quoted_spans().
CURLY_SPAN = re.compile("“([^”\\n]+?)”")


def quoted_spans(text: str) -> list[str]:
    """Every quotation on a line: straight quotes paired 1st-2nd, 3rd-4th…, curly by mark."""
    out: list[str] = []
    for line in text.split("\n"):
        idx = [i for i, ch in enumerate(line) if ch == '"']
        out.extend(line[a + 1 : b] for a, b in zip(idx[0::2], idx[1::2]))
        out.extend(m.group(1) for m in CURLY_SPAN.finditer(line))
    return out
EPIGRAPH = re.compile('^\\*["\u201c](.+?)["\u201d]\\*\\s*$')
# An em dash, en dash or double hyphen opens an attribution; a plain hyphen is a bullet.
ATTRIB = re.compile(
    "^\\*?(?:\u2014|\u2013|--)\\s*(?:after\\s+|from\\s+)?([A-Z][^,*\\n]{2,60}?)"
    "(?:,\\s*\\*?([^*\\n]{2,80}?)\\*?)?\\*?\\s*$"
)
KEYWORDS = {
    "lyrics": re.compile(r"\blyrics?\b", re.I),
    "transcript": re.compile(r"\btranscri(pt|bed)\b", re.I),
    "translated_by": re.compile(r"\b(translated by|trans\.|translation by)\b", re.I),
    "copyright_notice": re.compile(r"\u00a9|\(c\)\s*\d{4}|all rights reserved|copyright \d{4}", re.I),
    "verbatim": re.compile(r"\bverbatim\b", re.I),
}


def words(s: str) -> int:
    return len(s.split())


def scan(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    lines = text.split("\n")
    runs: list[int] = []
    cur = 0
    for ln in lines:
        if ln.lstrip().startswith(">"):
            cur += words(ln.lstrip("> ").strip())
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    epigraphs = [words(m.group(1)) for ln in lines if (m := EPIGRAPH.match(ln.strip()))]
    spans = [n for s in quoted_spans(text) if (n := words(s)) >= 40]
    attribs = []
    for ln in lines:
        m = ATTRIB.match(ln.strip())
        if m:
            attribs.append((m.group(1).strip(), (m.group(2) or "").strip()))
    flags = {k: len(rx.findall(text)) for k, rx in KEYWORDS.items() if rx.search(text)}
    shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    return {
        "path": str(shown).replace("\\", "/"),
        "words": words(text),
        "blockquote_words": sum(runs),
        "longest_run": max(runs, default=0),
        "runs_over_150": sum(1 for r in runs if r >= 150),
        "epigraph_words": sum(epigraphs),
        "epigraphs": len(epigraphs),
        "long_span_words": sum(spans),
        "long_spans": len(spans),
        "attributions": attribs,
        "flags": flags,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--min-words", type=int, default=300, help="verbatim words to list a file")
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    rows = [scan(p) for p in sorted((ROOT / "corpus").rglob("*.md"))]
    for r in rows:
        r["verbatim"] = r["blockquote_words"] + r["epigraph_words"] + r["long_span_words"]
    by_dir: dict[str, Counter] = {}
    for r in rows:
        d = r["path"].split("/")[1]
        c = by_dir.setdefault(d, Counter())
        c["files"] += 1
        c["words"] += r["words"]
        c["verbatim"] += r["verbatim"]
        c["flagged"] += r["verbatim"] >= a.min_words or r["longest_run"] >= 150
    print(f"{'dir':20} {'files':>5} {'words':>10} {'verbatim':>9} {'share':>6} {'flagged':>7}")
    for d, c in sorted(by_dir.items(), key=lambda kv: -kv[1]["verbatim"]):
        print(f"{d:20} {c['files']:5d} {c['words']:10,d} {c['verbatim']:9,d} {c['verbatim']/max(c['words'],1):6.1%} {c['flagged']:7d}")
    tot_v = sum(r["verbatim"] for r in rows)
    tot_w = sum(r["words"] for r in rows)
    print(f"\nTOTAL verbatim-signal words {tot_v:,} of {tot_w:,} ({tot_v/tot_w:.1%})")
    print(f"\nTop {a.top} files by verbatim signal:")
    for r in sorted(rows, key=lambda r: -r["verbatim"])[: a.top]:
        print(f"{r['verbatim']:7,d} bq={r['blockquote_words']:6,d} run={r['longest_run']:5d} ep={r['epigraphs']:3d} span={r['long_span_words']:5d} {r['flags']} {r['path']}")
    att = Counter(n for r in rows for n, _ in r["attributions"])
    print(f"\nTop attributed names ({sum(att.values())} attribution lines):")
    for n, k in att.most_common(50):
        print(f"{k:5d} {n}")
    if a.json:
        a.json.write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
