#!/usr/bin/env python3
"""
REFLECT-WORKLIST — the reflect pass's worklist and its check. Read-only.

The reflect pass hand-writes two kinds of passage: a *return passage* into an
older document the harvest cites but which never cites back, and a *meeting
passage* into a singleton naming the documents its constellation neighbourhood
already says it meets. This tool proposes; writers write the sentence. It
never links anything itself.

    python reflect-worklist.py                       print the worklist
    python reflect-worklist.py --out DIR             one markdown file per wave
    python reflect-worklist.py --per-wave 40         wave size (default 40)
    python reflect-worklist.py --check               re-measure
    python reflect-worklist.py --check --save-baseline b.json
    python reflect-worklist.py --check --baseline b.json     deltas

Waves group the proposable singletons (those with a constellation node) by
directory, directories ordered by summed type weight (forge's TYPE_WEIGHTS:
syntheses and bridges before glossary pages), and chunk them. The whole-graph
Cheeger constant is reported as 0.0 while any singleton remains, which is
exact: an isolated vertex has a zero-volume boundary.
"""

import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "notebooks"))
from linkgraph import Graph, doc_class, proposals, topdir  # noqa: E402

try:
    from forge import TYPE_WEIGHTS  # noqa: E402
except Exception:  # forge is optional; fall back to a flat weight
    TYPE_WEIGHTS = {}

HARVEST = ("corpus/seeds/", "corpus/synthesis/grown/", "corpus/synthesis/capstones/")


def weight(p: dict) -> float:
    return TYPE_WEIGHTS.get(p["type"], 0.4)


def waves(props: list, per_wave: int) -> list:
    by_dir = collections.defaultdict(list)
    for p in props:
        by_dir[p["dir"]].append(p)
    order = sorted(by_dir, key=lambda d: -sum(weight(p) for p in by_dir[d]))
    flat = []
    for d in order:
        flat.extend(sorted(by_dir[d], key=lambda p: (-weight(p), p["doc"])))
    return [flat[i:i + per_wave] for i in range(0, len(flat), per_wave)]


def returns(g: Graph, limit: int = 40) -> list:
    """Older documents ranked by harvest citations, with their back-edge count."""
    is_h = lambda p: any(p.startswith(x) for x in HARVEST)
    cited = collections.Counter()
    for s in g.docs:
        if is_h(s):
            for t in g.out[s]:
                if not is_h(t) and not t.startswith("corpus/threads/"):
                    cited[t] += 1
    rows = []
    for t, n in cited.most_common():
        back = sum(1 for x in g.out[t] if is_h(x))
        rows.append((t, n, back))
    rows.sort(key=lambda r: (-(r[1] - 3 * r[2]), r[0]))
    return rows[:limit]


def render(wave_list: list, ret: list) -> str:
    out = ["# Reflect worklist", "",
           "Proposals only. Each passage is hand-written in the document's own register, "
           "names the shared concept, and carries a sentence saying why.", ""]
    if ret:
        out.append("## Return passages (older documents the harvest cites; in / back)")
        for t, n, back in ret:
            out.append(f"- `{t}` — {n} in / {back} back")
    for i, w in enumerate(wave_list, 1):
        dirs = sorted({p["dir"] for p in w})
        out += ["", f"## Wave {i} — {len(w)} documents — {', '.join(d.split('/', 1)[1] for d in dirs)}"]
        for p in w:
            out.append(f"- `{p['doc']}`  [{p['node']}, {p['type']}]")
            for q in p["partners"]:
                out.append(f"    - meets `{q['doc']}` via **{q['via']}** ({q['score']})")
    return "\n".join(out) + "\n"


def check(g: Graph, baseline: dict | None) -> dict:
    sizes = g.components()
    singles = [d for d in g.docs if not g.inn[d] and not g.out[d]]
    with_node = sum(1 for d in singles if d in {v for v in g.node_doc.values()})
    c = g.conductance(list(HARVEST))
    multi, linked = g.bridge_share()
    now = dict(documents=len(g.docs), edges=sum(len(v) for v in g.out.values()),
               singletons=len(singles), singletons_with_node=with_node,
               back_edges=c["back"], harvest_conductance=round(c["conductance"], 3),
               bridge_share=round(multi / max(1, linked), 3), giant=sizes[0],
               cheeger=0.0 if singles else None)
    for k, v in now.items():
        delta = ""
        if baseline and k in baseline and isinstance(v, (int, float)) and isinstance(baseline[k], (int, float)):
            delta = f"   ({baseline[k]} -> {v}, {v - baseline[k]:+})"
        print(f"{k:22} {v}{delta}")
    if singles:
        print("cheeger is exactly 0.0 while any singleton remains; the harvest figure is a local conductance")
    return now


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out")
    ap.add_argument("--per-wave", type=int, default=40)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--baseline")
    ap.add_argument("--save-baseline")
    args = ap.parse_args()
    g = Graph()
    if args.check:
        base = json.loads(Path(args.baseline).read_text(encoding="utf-8")) if args.baseline else None
        now = check(g, base)
        if args.save_baseline:
            Path(args.save_baseline).parent.mkdir(parents=True, exist_ok=True)
            Path(args.save_baseline).write_text(json.dumps(now, indent=1), encoding="utf-8")
        return
    wave_list = waves(proposals(g, 0), args.per_wave)
    text = render(wave_list, returns(g))
    if args.out:
        Path(args.out).mkdir(parents=True, exist_ok=True)
        (Path(args.out) / "00-return-passages.md").write_text(render([], returns(g)), encoding="utf-8")
        for i, w in enumerate(wave_list, 1):
            (Path(args.out) / f"wave-{i:02d}.md").write_text(render([w], []), encoding="utf-8")
        print(f"wrote {len(wave_list)} wave files to {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
