#!/usr/bin/env python3
"""
wire_documents.py — After the sweep agents finish, this scans for written docs
and adds the corresponding `document` field to each constellation node.

For each entry in cli/output/sweep-manifest.json:
  - If output_path file exists on disk, set node.document = output_path
  - If missing, log it to a failures list

Output: prints summary; updates constellation.json in-place.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    manifest = json.loads((ROOT / "cli" / "output" / "sweep-manifest.json").read_text())
    cpath = ROOT.parent / "constellation" / "constellation.json"
    data = json.loads(cpath.read_text())
    nodes = data.get("nodes", data)

    written = []
    missing = []
    skipped_existing = []

    for entry in manifest:
        nid = entry["node_id"]
        out_rel = entry["output_path"]
        out_abs = ROOT / out_rel
        if not out_abs.exists():
            missing.append((nid, out_rel))
            continue
        node = nodes.get(nid)
        if not node:
            missing.append((nid, "node not found"))
            continue
        if node.get("document"):
            skipped_existing.append((nid, node["document"]))
            continue
        node["document"] = out_rel
        written.append((nid, out_rel))

    if "nodes" in data:
        data["nodes"] = nodes
    else:
        data = nodes
    cpath.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print(f"=== wire_documents summary ===")
    print(f"  wired:           {len(written)}")
    print(f"  missing on disk: {len(missing)}")
    print(f"  already wired:   {len(skipped_existing)}")
    if missing:
        print(f"\nMissing docs (will not be wired):")
        for nid, p in missing:
            print(f"  - {nid}: {p}")
    if skipped_existing:
        print(f"\nAlready had document field:")
        for nid, p in skipped_existing[:8]:
            print(f"  - {nid}: {p}")


if __name__ == "__main__":
    main()
