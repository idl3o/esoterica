#!/usr/bin/env python3
"""
RELINK — repair dead relative links. Proposes by default; writes only with --apply.

Consumes the dead-link list the harness finds (linkgraph.Graph().dead) and, for
each, looks for the one file in the repository with that basename. Three
outcomes:

    fixed      exactly one file has the basename -> corrected relative path
    ambiguous  several files share it            -> reported, never guessed
    missing    no file has it                    -> reported as truly dead

    python relink.py            diff-style report
    python relink.py --apply    rewrite the fixed ones in place (CRLF-safe)
    python relink.py --json     machine-readable report

The basename index skips .git, node_modules, dist and __pycache__: the site's
dist/ mirrors the whole corpus and would make every name ambiguous.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict, namedtuple
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkgraph import REPO, Graph  # noqa: E402

SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__", ".astro"}

Fix = namedtuple("Fix", "src href kind new_href candidates")


def index_basenames():
    """basename -> [repo-relative paths], pruning SKIP_DIRS."""
    index = defaultdict(list)
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                index[f].append(Path(root, f).relative_to(REPO).as_posix())
    return index


def relative_href(src: str, target: str) -> str:
    return Path(os.path.relpath(REPO / target, (REPO / src).parent)).as_posix()


def propose(g: Graph, index) -> list:
    fixes, seen = [], set()
    for src, href in g.dead:
        if (src, href) in seen:
            continue
        seen.add((src, href))
        hits = index.get(Path(href).name, [])
        if len(hits) == 1:
            fixes.append(Fix(src, href, "fixed", relative_href(src, hits[0]), hits))
        elif hits:
            fixes.append(Fix(src, href, "ambiguous", None, sorted(hits)))
        else:
            fixes.append(Fix(src, href, "missing", None, []))
    return sorted(fixes, key=lambda f: (f.kind, f.src, f.href))


def report(fixes) -> None:
    by = defaultdict(list)
    for f in fixes:
        by[f.kind].append(f)
    for f in by["fixed"]:
        print(f"-  {f.src}: ]({f.href})\n+  {f.src}: ]({f.new_href})")
    if by["ambiguous"]:
        print("\nambiguous (ruling needed, nothing changed):")
        for f in by["ambiguous"]:
            print(f"   {f.src}: ]({f.href})  ->  {f.candidates}")
    if by["missing"]:
        print("\nmissing (no file with that name anywhere):")
        for f in by["missing"]:
            print(f"   {f.src}: ]({f.href})")
    print(f"\n{len(by['fixed'])} fixed  {len(by['ambiguous'])} ambiguous  {len(by['missing'])} missing",
          file=sys.stderr)


def apply(fixes) -> None:
    touched = defaultdict(list)
    for f in fixes:
        if f.kind == "fixed":
            touched[f.src].append(f)
    for src, items in touched.items():
        path = REPO / src
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        for f in items:
            text = re.sub(r"\]\(" + re.escape(f.href) + r"(?=[#)])", "](" + f.new_href, text)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        print(f"rewrote {len(items)} link(s) in {src}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--include-slate", action="store_true")
    args = ap.parse_args()
    fixes = propose(Graph(include_slate=args.include_slate), index_basenames())
    if args.json:
        json.dump([f._asdict() for f in fixes], sys.stdout, indent=1)
    else:
        report(fixes)
    if args.apply:
        apply(fixes)


if __name__ == "__main__":
    main()
