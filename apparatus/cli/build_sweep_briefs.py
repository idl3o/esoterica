#!/usr/bin/env python3
"""
build_sweep_briefs.py — Emit one JSON brief per worklist node for the Phase 3 sweep.

Each brief has everything the per-node author agent needs:
- node id, type, essence, description
- list of {connected_id, type, essence, description} for context
- pre-assigned output path
- repo-root path

Output: cli/output/sweep-briefs.json (array of briefs)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Type → output directory mapping (Phase 3 of plan)
TYPE_DIR = {
    "cosmological":             "synthesis/cosmological",
    "archetype":                "synthesis/archetypal",
    "consciousness_technology": "synthesis/consciousness-technologies",
    "concept":                  "synthesis/concepts",
    "process":                  "synthesis/processes",
    "framework":                "synthesis/frameworks",
    "glyph":                    "synthesis/glyphs",
    "tradition":                "synthesis/traditions",
    "architecture":             "synthesis/architectures",
    "meta_system":              "synthesis/meta-systems",
    "recognition":              "synthesis/recognitions",
    "practice":                 "synthesis/practices",
    "phenomenon":               "synthesis/phenomena",
    "element":                  "synthesis/elements",
    "collective":               "synthesis/collectives",
    "application":              "synthesis/applications",
}


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    work = json.loads((ROOT / "cli" / "output" / "empty-powerful-nodes.json").read_text())
    nodes = json.loads((ROOT.parent / "constellation" / "constellation.json").read_text())
    nodes = nodes.get("nodes", nodes)

    briefs = []
    for w in work:
        nid = w["id"]
        node = nodes[nid]
        # gather connection metadata
        conns = []
        for cid in node.get("connections", []):
            cn = nodes.get(cid)
            if cn:
                conns.append({
                    "id": cid,
                    "type": cn.get("type", "?"),
                    "essence": cn.get("essence", ""),
                    "description": (cn.get("description") or "")[:400],
                })
            else:
                conns.append({"id": cid, "type": "?", "essence": "", "description": ""})

        out_dir = TYPE_DIR.get(node.get("type"), f"synthesis/{node.get('type', 'misc')}")
        out_path = f"{out_dir}/{slugify(nid)}.md"

        briefs.append({
            "node_id": nid,
            "type": node.get("type"),
            "essence": node.get("essence"),
            "description": node.get("description", ""),
            "connection_count": len(conns),
            "connections": conns,
            "output_path": out_path,
            "absolute_output_path": str(ROOT / out_path),
        })

    # ensure output dirs exist
    for b in briefs:
        Path(b["absolute_output_path"]).parent.mkdir(parents=True, exist_ok=True)

    out_file = ROOT / "cli" / "output" / "sweep-briefs.json"
    out_file.write_text(json.dumps(briefs, indent=2))

    # also emit a flat dispatch summary
    summary = ROOT / "cli" / "output" / "sweep-dispatch-summary.txt"
    lines = [f"{'connections':>4}  {'type':28s}  {'output_path':70s}  node_id"]
    lines.append("-" * 130)
    for b in briefs:
        lines.append(f"{b['connection_count']:4d}  {b['type']:28s}  {b['output_path']:70s}  {b['node_id']}")
    summary.write_text("\n".join(lines) + "\n")

    print(f"emitted {len(briefs)} briefs → {out_file.relative_to(ROOT)}", file=sys.stderr)
    print(f"dispatch summary       → {summary.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
