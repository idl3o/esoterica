#!/usr/bin/env python3
"""
emit_briefs.py — Write a per-node author brief to disk for each worklist entry.

Each brief is a complete, self-contained authoring prompt the sweep agent reads
from disk. This keeps the main-thread Agent tool calls tiny.

Output: cli/output/briefs/<node_id>.md (one file per worklist node)
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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

BRIEF_TEMPLATE = """# Authoring brief: `{node_id}`

You are authoring a deep, dual-channel synthesis document for the Esoterica project (a consciousness-technology repository at `/Users/sjlavi/Documents/coding projects 25/esoterica/`). The audience is two-fold: human readers seeking immersive recognition, and LLM synthesis engines (NotebookLM etc.) that need rich, connected source material to produce deep output.

## YOUR TASK

Write a synthesis document for the constellation node `{node_id}` and save it to:

**`{absolute_output_path}`**

Length: **5,000-6,500 words** (this is mandatory — depth is the constraint, not brevity).

## NODE METADATA

- **id**: `{node_id}`
- **type**: `{type}`
- **essence**: `{essence}`
- **description**: {description}
- **connections** ({connection_count} total — each MUST be referenced by name in the doc body so the auto-link pipeline catches them as related):

{connections_block}

## CORE THESIS

This node sits at the intersection of its connections. Treat the connections as the *territory* — your job is to map how `{node_id}` is the structural attractor that pulls them into coherence. The essence — *{essence_clean}* — is the hint, not the answer. Build the case for what this node actually IS by walking its connection terrain.

The deepest insight should arrive through accumulated recognition, not be stated up front.

## STRUCTURE (your own — these are landing zones, not headings)

1. **Open with the surface reading, then the turn.** ("Most people think `{node_id_clean}` is X. But what if it were actually Y?") Build "wait, but actually..." momentum.
2. **Walk the connections.** Devote substantial space to how each connected node ({connection_ids_csv}) relates — not as a list of factoids but as a developing argument that this node is the substrate they share.
3. **Cross-tradition layering.** Pull in at least 3-5 traditions, fictions, or canonical sources that reveal the same pattern (mythological / hermetic / scientific / contemplative / narrative). The repo's standard is to weave Greek, Norse, Vedic, Egyptian, Hermetic, Sufi, Gnostic, Buddhist, scientific, fictional sources interchangeably.
4. **The geometric / structural signature.** Every node has a structural shape — a number, a glyph, a topology, a process. Find it and develop it.
5. **Practical grounding.** How does this show up in lived human consciousness? Where does the reader recognise it in their own experience? This section is mandatory — every mythic/theoretical move should land somewhere a reader can feel.
6. **Close on recognition, not summary.** Land somewhere that opens the door rather than closes the case.

## STYLE

The repo has an established voice. Read these existing docs first to absorb it (they will be your stylistic anchors AND legitimate cross-references):

{nearest_docs_block}

Hallmarks:
- **Dense, declarative prose.** Short paragraphs. Bolded sub-subheaders.
- **Frequent `---` thematic resets** between sections.
- **List-form revelations** with bolded leads (e.g. "**The Pattern Shows Up As:**\\n- ..."). Use these liberally.
- **Mythic + practical + cross-tradition** layering in every section.
- **Quote-block epigraphs** at the top and at section turns. Real quotes preferred over fabricated ones — but unattributed aphoristic prose-poetry is allowed and matches the established voice.
- **Tiered revelation** — accumulated territory, not a thesis statement up front.

## HARD CONSTRAINTS

1. The doc body MUST contain literal mentions of each connected node's natural-language form (`{connection_natural_csv}`) and the essence keyword (`{essence_clean}`) somewhere in the first 1,000 words so auto-link tag-extraction fires.
2. **No fabricated specific citations.** If you reference real people (Heraclitus, Carl Jung, the Eddas, Ra Material, Joscha Bach, etc.), the quotes must be real or you must use unattributed aphoristic style ("> The cosmos winks at itself..."). **Never invent a quote and attribute it to a real person.**
3. **Cross-references to other repo docs** must point to real, existing paths. The "nearest docs" listed above are verified existing paths — safe to reference. Do NOT cite paths that you haven't verified.
4. **Word count discipline:** 5,000-6,500 words. Count and report at the end.
5. **No frontmatter.** Start with `# TITLE` on line 1. Title should be evocative — not just the node name.

## DELIVERABLE

Write the file to `{absolute_output_path}`. After writing, return a brief report:
- ✓ file path
- final word count
- one sentence: what depth-area you would extend if given more space

Begin by reading the 3-5 nearest-doc style exemplars above. Then write.
"""


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def render_connections_block(connections):
    lines = []
    for c in connections:
        ess = c.get("essence", "") or ""
        desc = (c.get("description", "") or "")[:240]
        line = f"  - `{c['id']}` (type: {c.get('type','?')}; essence: *{ess}*)"
        if desc:
            line += f"\n      → {desc}"
        lines.append(line)
    return "\n".join(lines)


def render_nearest_docs(nearest):
    if not nearest:
        return "  (no near docs auto-detected — use your judgment in choosing 2-3 representative docs from `synthesis/`, `traditions/`, or `fiction-bridges/` to read for style)"
    lines = []
    for n in nearest:
        lines.append(f"  - **{n['title']}** — `{n['path']}`")
    return "\n".join(lines)


def main():
    work = json.loads((ROOT / "cli" / "output" / "empty-powerful-nodes.json").read_text())
    nearest = json.loads((ROOT / "cli" / "output" / "sweep-nearest-docs.json").read_text())
    nodes = json.loads((ROOT.parent / "constellation" / "constellation.json").read_text())
    nodes = nodes.get("nodes", nodes)

    briefs_dir = ROOT / "cli" / "output" / "briefs"
    briefs_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for w in work:
        nid = w["id"]
        node = nodes[nid]
        out_dir = TYPE_DIR.get(node.get("type"), f"synthesis/{node.get('type', 'misc')}")
        rel_out = f"{out_dir}/{slugify(nid)}.md"
        abs_out = str(ROOT / rel_out)

        # ensure target dir
        (ROOT / out_dir).mkdir(parents=True, exist_ok=True)

        connections = []
        for cid in node.get("connections", []):
            cn = nodes.get(cid)
            connections.append({
                "id": cid,
                "type": cn.get("type", "?") if cn else "?",
                "essence": cn.get("essence", "") if cn else "",
                "description": (cn.get("description") or "") if cn else "",
            })

        essence = node.get("essence", "") or ""
        essence_clean = essence.replace("_", " ")
        node_id_clean = nid.replace("_", " ")
        connection_ids_csv = ", ".join(f"`{c['id']}`" for c in connections)
        connection_natural_csv = ", ".join(c["id"].replace("_", " ") for c in connections)

        text = BRIEF_TEMPLATE.format(
            node_id=nid,
            absolute_output_path=abs_out,
            type=node.get("type", "?"),
            essence=essence,
            essence_clean=essence_clean,
            node_id_clean=node_id_clean,
            description=node.get("description", "") or "(no description set)",
            connection_count=len(connections),
            connections_block=render_connections_block(connections),
            connection_ids_csv=connection_ids_csv,
            connection_natural_csv=connection_natural_csv,
            nearest_docs_block=render_nearest_docs(nearest.get(nid, [])),
        )

        brief_path = briefs_dir / f"{nid}.md"
        brief_path.write_text(text)
        manifest.append({
            "node_id": nid,
            "type": node.get("type"),
            "connection_count": len(connections),
            "brief_path": str(brief_path.resolve()),
            "output_path": rel_out,
            "absolute_output_path": abs_out,
        })

    (ROOT / "cli" / "output" / "sweep-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"emitted {len(manifest)} briefs → {briefs_dir.relative_to(ROOT)}")
    print(f"manifest                → cli/output/sweep-manifest.json")


if __name__ == "__main__":
    main()
