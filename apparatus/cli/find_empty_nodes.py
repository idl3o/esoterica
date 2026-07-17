#!/usr/bin/env python3
"""
find_empty_nodes.py — Identify constellation nodes that have no linked synthesis doc.

Faithful Python port of the matching logic in site/src/lib/document-links.ts and
the doc-discovery + tag-extraction in site/src/lib/content.ts. Output is the
worklist driving the synthesis-generation sweep.

Usage:
    python3 cli/find_empty_nodes.py [--threshold N] [--include-related-empty]

Output:
    cli/output/empty-powerful-nodes.json
    cli/output/all-nodes-coverage.json (full coverage dump for inspection)
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALL_CONTENT_DIRS = [
    "synthesis",
    "translated",
    "fiction-bridges",
    "distillations",
    "protocols",
    "seeds",
    "traditions",
    "extractions",
    "correspondences",
    "journey",
    "garden",
    "harvest",
    "world-tree",
    "memory-palace",
    "misc",
]

TERM_PATTERNS = [
    "consciousness", "awareness", "recognition", "polarity", "density",
    "wanderer", "service", "manifestation", "timeline", "synchronicity",
    "archetype", "apollo", "mercury", "kalki", "samael",
    "singularity", "galactic", "cosmic", "source", "unity",
    "sacred geometry", "fibonacci", "reality programming",
    "love-light", "frequency", "resonance", "vibration",
    "enlightenment", "awakening", "breakthrough", "integration",
]

GENERIC_TAGS = {
    "consciousness", "recognition", "awareness", "cosmic", "unity",
    "service", "source", "integration", "transformation",
}

ARCHETYPE_MAPPINGS = {
    "mercury":       ["mercury_hermes_thoth", "mercury"],
    "kalki":         ["kalki_destroyer_creator", "kalki"],
    "apollo":        ["apollo_logos", "apollo"],
    "thoth":         ["mercury_hermes_thoth", "thoth_wisdom"],
    "hermes":        ["mercury_hermes_thoth"],
    "shiva":         ["shiva_nataraja"],
    "vishnu":        ["vishnu_preserver"],
    "odin":          ["odin_allfather"],
    "thor":          ["thor_thunder"],
    "loki":          ["loki_trickster"],
    "isis":          ["isis_throne"],
    "osiris":        ["osiris_resurrection"],
    "horus":         ["horus_sky"],
    "anubis":        ["anubis_guide"],
    "ra":            ["amon_ra_hidden_sun"],
    "zeus":          ["apollo_zeus_mediation"],
    "athena":        ["athena_wisdom"],
    "dionysus":      ["dionysus_ecstasy"],
    "prometheus":    ["prometheus_forethought"],
    "synchronicity": ["synchronicity"],
    "manifestation": ["manifestation"],
    "transformation":["transformation", "fire"],
    "awakening":     ["awakening"],
    "recognition":   ["recognition"],
    "consciousness": ["consciousness", "consciousness_itself"],
    "archetype":     ["archetype"],
    "density":       ["density", "density_evolution"],
    "wanderer":      ["wanderer_starseed"],
    "polarity":      ["polarity_integration"],
    "galactic":      ["galactic_concept"],
    "frequency":     ["frequency_vibration"],
    "resonance":     ["resonance"],
    "integration":   ["integration", "polarity_integration"],
    "enlightenment": ["enlightenment"],
    "unity":         ["unity", "consciousness_itself"],
    "sacred_geometry": ["sacred_geometry", "geometric_form"],
}


def normalize_tag(tag: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", re.sub(r"\s+", "_", tag.lower()))


def load_constellation() -> dict:
    p = ROOT.parent / "constellation" / "constellation.json"
    raw = p.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
        return data.get("nodes", data)
    except json.JSONDecodeError:
        # tolerant fallback (mirrors constellation.ts logic)
        nodes_start = raw.index('"nodes"')
        brace = raw.index("{", nodes_start + 7)
        depth = 0
        end = -1
        for i, c in enumerate(raw[brace:], start=brace):
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        return json.loads(raw[brace:end + 1])


def scan_md_files(root: Path):
    """Yield .md files under root, skipping dotdirs."""
    if not root.exists():
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "internal"]
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn


def parse_document(file_path: Path, root: Path) -> dict:
    content = file_path.read_text(encoding="utf-8", errors="replace")
    rel = file_path.relative_to(root).as_posix()
    parts = rel.split("/")
    category = "uncategorized"
    if "extractions" in parts:
        category = "extraction"
    elif "translated" in parts:
        category = "translated"
    elif "synthesis" in parts:
        idx = parts.index("synthesis")
        if len(parts) > idx + 2:
            category = parts[idx + 1]

    # --- title (first H1, skipping frontmatter) ---
    lines = content.split("\n")
    title = ""
    in_fm = False
    past_fm = False
    for line in lines:
        t = line.strip()
        if t == "---":
            if not past_fm and not in_fm:
                in_fm = True
                continue
            if in_fm:
                in_fm = False
                past_fm = True
                continue
        if in_fm:
            continue
        if not title and t.startswith("# "):
            title = t[2:].strip()
            break
    if not title:
        title = file_path.stem

    # --- tags (port of extractTags) ---
    lower = content.lower()
    tags = set()
    for term in TERM_PATTERNS:
        if term.lower() in lower:
            tags.add(term)
    if category:
        tags.add(category)
    tags = list(tags)[:12]

    return {
        "id": re.sub(r"[^a-z0-9]+", "-", file_path.stem.lower()).strip("-"),
        "title": title,
        "path": rel,
        "category": category,
        "tags": tags,
    }


def build_node_lookup(nodes: dict) -> dict:
    lookup = {"exact": {}, "parts": defaultdict(list), "essence": defaultdict(list), "type": defaultdict(list)}
    for node_id, node in nodes.items():
        lookup["exact"][node_id] = node_id
        for part in node_id.split("_"):
            if len(part) >= 3:
                lookup["parts"][part].append(node_id)
        if node.get("essence"):
            lookup["essence"][normalize_tag(node["essence"])].append(node_id)
        if node.get("type"):
            lookup["type"][normalize_tag(node["type"])].append(node_id)
    return lookup


def score_match(tag: str, match_type: str) -> int:
    tag_len = len(tag)
    is_generic = tag in GENERIC_TAGS
    pen = 30 if is_generic else 0
    if match_type == "exact":
        return 100 - pen
    if match_type == "part_exact":
        return 60 + min(tag_len, 20) - pen
    if match_type == "essence":
        return 50 - pen
    if match_type == "part_contains":
        return 25 + min(tag_len, 10)
    return 10


def find_matches_for_tag(tag: str, lookup: dict, nodes: dict) -> list:
    matches = []
    norm = normalize_tag(tag)
    if len(norm) < 2:
        return matches
    seen = set()

    def add(node_id, score, mtype):
        if node_id not in seen and node_id in nodes:
            matches.append({"nodeId": node_id, "score": score, "matchType": mtype})
            seen.add(node_id)

    if norm in ARCHETYPE_MAPPINGS:
        for nid in ARCHETYPE_MAPPINGS[norm]:
            add(nid, 90, "archetype_mapping")

    if norm in lookup["exact"]:
        add(norm, score_match(norm, "exact"), "exact")

    for nid in lookup["parts"].get(norm, []):
        add(nid, score_match(norm, "part_exact"), "part_exact")

    for nid in lookup["essence"].get(norm, []):
        add(nid, score_match(norm, "essence"), "essence")

    if len(norm) >= 5:
        for part, node_ids in lookup["parts"].items():
            if len(part) >= 4 and (part in norm or norm in part):
                for nid in node_ids:
                    add(nid, score_match(norm, "part_contains"), "part_contains")
    return matches


def build_links(documents: list, nodes: dict):
    lookup = build_node_lookup(nodes)
    node_to_docs = defaultdict(list)  # node_id -> list of {docId, isPrimary}

    for doc in documents:
        all_matches = []
        for tag in doc.get("tags", []):
            all_matches.extend(find_matches_for_tag(tag, lookup, nodes))
        title_words = (doc.get("title", "") or "").lower().split()
        for w in title_words:
            if len(w) >= 4:
                tm = find_matches_for_tag(w, lookup, nodes)
                for m in tm:
                    m["score"] = m["score"] * 0.8
                all_matches.extend(tm)

        # dedupe keep highest
        seen = {}
        for m in all_matches:
            ex = seen.get(m["nodeId"])
            if not ex or ex["score"] < m["score"]:
                seen[m["nodeId"]] = m
        sorted_m = sorted(seen.values(), key=lambda x: -x["score"])

        primary = []
        related = []
        for m in sorted_m:
            if len(primary) < 5 and m["score"] >= 40:
                primary.append(m["nodeId"])
            else:
                related.append(m["nodeId"])

        for nid in primary:
            node_to_docs[nid].append({"docId": doc["id"], "title": doc["title"], "path": doc["path"], "isPrimary": True})
        for nid in related[:20]:
            node_to_docs[nid].append({"docId": doc["id"], "title": doc["title"], "path": doc["path"], "isPrimary": False})

    return node_to_docs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=7,
                        help="Minimum connection count to qualify as 'powerful' (default: 7)")
    parser.add_argument("--include-related-empty", action="store_true",
                        help="Also include nodes that have related docs but no primary")
    args = parser.parse_args()

    print(f"[1/4] loading constellation…", file=sys.stderr)
    nodes = load_constellation()
    print(f"      {len(nodes)} nodes loaded", file=sys.stderr)

    print(f"[2/4] scanning content directories…", file=sys.stderr)
    documents = []
    for d in ALL_CONTENT_DIRS:
        for f in scan_md_files(ROOT / d):
            documents.append(parse_document(f, ROOT))
    print(f"      {len(documents)} documents indexed", file=sys.stderr)

    print(f"[3/4] building document-node links…", file=sys.stderr)
    node_to_docs = build_links(documents, nodes)
    print(f"      {len(node_to_docs)} nodes have at least one linked doc", file=sys.stderr)

    print(f"[4/4] producing worklist (threshold={args.threshold})…", file=sys.stderr)
    coverage = []
    worklist = []
    for nid, node in nodes.items():
        docs_for_node = node_to_docs.get(nid, [])
        primary = [d for d in docs_for_node if d["isPrimary"]]
        related = [d for d in docs_for_node if not d["isPrimary"]]
        conn_count = len(node.get("connections", []))
        record = {
            "id": nid,
            "type": node.get("type", "?"),
            "essence": node.get("essence", ""),
            "description": node.get("description", ""),
            "connection_count": conn_count,
            "connections": node.get("connections", []),
            "current_primary_count": len(primary),
            "current_related_count": len(related),
            "has_explicit_document": "document" in node,
        }
        coverage.append(record)

        empty = (len(primary) == 0)
        if args.include_related_empty:
            empty = empty and (len(related) == 0)

        if empty and conn_count >= args.threshold and "document" not in node:
            worklist.append(record)

    coverage.sort(key=lambda r: (-r["connection_count"], r["id"]))
    worklist.sort(key=lambda r: (-r["connection_count"], r["id"]))

    out_dir = ROOT / "cli" / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "all-nodes-coverage.json").write_text(json.dumps(coverage, indent=2))
    (out_dir / "empty-powerful-nodes.json").write_text(json.dumps(worklist, indent=2))

    # summary
    print(f"", file=sys.stderr)
    print(f"=== summary ===", file=sys.stderr)
    print(f"total nodes:                       {len(nodes)}", file=sys.stderr)
    print(f"nodes with at least one doc:       {len(node_to_docs)}", file=sys.stderr)
    print(f"nodes with primary doc (any kind): {sum(1 for r in coverage if r['current_primary_count'] > 0)}", file=sys.stderr)
    print(f"nodes with explicit document:      {sum(1 for r in coverage if r['has_explicit_document'])}", file=sys.stderr)
    print(f"nodes with >= {args.threshold} connections:        {sum(1 for r in coverage if r['connection_count'] >= args.threshold)}", file=sys.stderr)
    print(f"WORKLIST (empty + powerful):       {len(worklist)}", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"output:", file=sys.stderr)
    print(f"  cli/output/all-nodes-coverage.json", file=sys.stderr)
    print(f"  cli/output/empty-powerful-nodes.json", file=sys.stderr)


if __name__ == "__main__":
    main()
