#!/usr/bin/env python3
"""
FORGE — bundle generation for the NotebookLM synthesis laboratory.

Turns the constellation graph into a salience engine and a bundle assembler.

    python forge.py salience [--interest TERM ...] [-n 25]
    python forge.py bundle SEED_NODE [--name SLUG] [--size 10] [--interest TERM ...]
    python forge.py info SEED_NODE

`salience` ranks document-bearing nodes by how ripe they are for a deep dive.
`bundle` grows a source bundle outward from a seed node, mines the concept
convergences between the chosen sources, and scaffolds PROMPT.md plus a
measurement checklist. Sources are copied into bundles/<slug>/sources/ ready
for drag-and-drop upload.

The scoring model (weights below):
  degree        — how connected the node is (log-scaled)
  bridge        — how many distinct node types its neighbourhood spans;
                  cross-domain connectors make the deepest audio
  doc_rich      — how many neighbours also carry documents (a bundle needs
                  8-15 sources, so a seed needs a document-rich neighbourhood)
  recency       — git last-touch date of the document (interest proxy)
  novelty       — penalty if the document already appears in an existing bundle
  interest      — optional user-supplied terms matched against id/essence/
                  connections/path
"""

import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent          # apparatus/notebooks
REPO = HERE.parent.parent                       # repo root
CORPUS = REPO / "corpus"
CONSTELLATION = REPO / "constellation" / "constellation.json"
BUNDLES = HERE / "bundles"
LOG = HERE / "experiments" / "LOG.md"

WEIGHTS = {
    "degree": 1.0,
    "bridge": 1.5,
    "doc_rich": 1.5,
    "type": 2.0,
    "recency": 1.0,
    "novelty": 2.0,     # subtracted when already bundled
    "interest": 3.0,    # per matched term, capped at 2 terms
}

# Degree sweet spot: a deep-dive seed wants a *specific* document with a rich
# but bounded neighbourhood. Extreme hubs (transformation, light, ...) connect
# to everything, so a bundle grown from one has no coherent theme. The degree
# score is a bell over log(degree) peaking here and decaying on both sides.
DEGREE_SWEET_SPOT = 20

# Specific, substantial material makes deep dives; glossary hubs (concept,
# element, state, process, glyph) make shallow ones. Unlisted types get 0.4.
TYPE_WEIGHTS = {
    "fiction_bridge": 1.0, "synthesis": 0.95, "distillation": 0.95,
    "grown_synthesis": 0.95, "translation": 0.85, "extraction": 0.85,
    "protocol": 0.8, "cosmological": 0.8, "journey": 0.75,
    "tradition": 0.7, "correspondence": 0.7, "archetype": 0.7,
    "architecture": 0.7, "framework": 0.7, "meta_system": 0.6,
    "consciousness_technology": 0.6, "seed": 0.5,
    "concept": 0.15, "element": 0.15, "state": 0.15, "process": 0.15,
    "glyph": 0.1, "collective": 0.3,
}


# ---------------------------------------------------------------- graph load

def load_graph():
    data = json.loads(CONSTELLATION.read_text(encoding="utf-8"))
    nodes = data["nodes"]
    incoming = Counter()
    for nid, node in nodes.items():
        for target in node.get("connections", []):
            incoming[target] += 1
    adjacency = {}
    for nid, node in nodes.items():
        adjacency.setdefault(nid, set()).update(node.get("connections", []))
        for target in node.get("connections", []):
            adjacency.setdefault(target, set()).add(nid)
    return nodes, incoming, adjacency


def doc_path(node):
    doc = node.get("document")
    if not doc:
        return None
    p = CORPUS / doc
    return p if p.exists() else None


def git_recency_map():
    """Map corpus-relative doc path -> unix time of most recent commit."""
    try:
        out = subprocess.run(
            ["git", "log", "--pretty=%x01%ct", "--name-only"],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=True,
        ).stdout
    except Exception:
        return {}
    recency, current = {}, None
    for line in out.splitlines():
        if line.startswith("\x01"):
            current = int(line[1:])
        elif line.strip() and current is not None:
            path = line.strip()
            if path.startswith("corpus/") and path not in recency:
                recency[path] = current
    return recency


def already_bundled_paths():
    """Corpus-relative paths referenced by any existing bundle PROMPT.md."""
    used = set()
    for prompt in BUNDLES.glob("*/PROMPT.md"):
        text = prompt.read_text(encoding="utf-8", errors="replace")
        for match in re.findall(r"\(([^)]+\.md)\)", text):
            cleaned = re.sub(r"^(\.\./)+", "", match).lstrip("/")
            used.add(cleaned)
    return used


# ------------------------------------------------------------------ salience

def score_nodes(nodes, incoming, adjacency, interest_terms):
    recency = git_recency_map()
    used = already_bundled_paths()
    times = sorted(recency.values())
    t_min, t_max = (times[0], times[-1]) if times else (0, 1)

    scored = []
    for nid, node in nodes.items():
        p = doc_path(node)
        if not p:
            continue
        neighbours = adjacency.get(nid, set())
        degree = len(neighbours) + incoming.get(nid, 0)
        n_types = {nodes[m]["type"] for m in neighbours if m in nodes}
        doc_neighbours = [m for m in neighbours if m in nodes and doc_path(nodes[m])]

        s_degree = math.exp(
            -((math.log1p(degree) - math.log1p(DEGREE_SWEET_SPOT)) ** 2) / 0.8
        )
        s_type = TYPE_WEIGHTS.get(node["type"], 0.4)
        s_bridge = min(len(n_types) / 8.0, 1.0)
        s_docrich = min(len(doc_neighbours) / 10.0, 1.0)
        rel = node["document"]
        t = recency.get("corpus/" + rel.replace("\\", "/"))
        s_recency = (t - t_min) / (t_max - t_min) if t and t_max > t_min else 0.0
        s_novelty = 1.0 if rel.replace("\\", "/") in {u.removeprefix("corpus/") for u in used} else 0.0

        haystack = " ".join(
            [nid, node.get("essence", ""), node.get("type", ""), rel]
            + list(node.get("connections", []))
        ).lower()
        matched = [term for term in interest_terms if term.lower() in haystack]
        s_interest = min(len(matched), 2)

        total = (
            WEIGHTS["degree"] * s_degree
            + WEIGHTS["type"] * s_type
            + WEIGHTS["bridge"] * s_bridge
            + WEIGHTS["doc_rich"] * s_docrich
            + WEIGHTS["recency"] * s_recency
            - WEIGHTS["novelty"] * s_novelty
            + WEIGHTS["interest"] * s_interest
        )
        scored.append({
            "id": nid, "score": total, "type": node["type"],
            "essence": node.get("essence", ""), "document": rel,
            "degree": degree, "types_spanned": len(n_types),
            "doc_neighbours": len(doc_neighbours),
            "bundled": bool(s_novelty), "matched": matched,
        })
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored


def cmd_salience(args):
    nodes, incoming, adjacency = load_graph()
    scored = score_nodes(nodes, incoming, adjacency, args.interest or [])
    print(f"{'score':>6}  {'deg':>4} {'span':>4} {'docs':>4}  node")
    for row in scored[: args.n]:
        flags = " [bundled]" if row["bundled"] else ""
        flags += f" [{','.join(row['matched'])}]" if row["matched"] else ""
        print(
            f"{row['score']:6.2f}  {row['degree']:4d} {row['types_spanned']:4d} "
            f"{row['doc_neighbours']:4d}  {row['id']}  ({row['type']}: "
            f"{row['essence']}){flags}"
        )
        print(f"{'':24}corpus/{row['document']}")


# ---------------------------------------------------------------- treatment

def strip_decoration(text):
    """Clean a source copy for NotebookLM ingestion.

    Removes YAML frontmatter, drops pure-glyph decoration lines (non-ASCII
    symbol runs with no letters — ASCII rules and table separators survive),
    and flattens markdown links to their text so cross-references read as
    prose instead of dead relative URLs.
    """
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end = lines[1:].index("---") + 1
            lines = lines[end + 1:]
        except ValueError:
            pass
    kept = []
    for line in lines:
        s = line.strip()
        if s and not re.search(r"[A-Za-z0-9]", s) and any(ord(c) > 127 for c in s):
            continue
        kept.append(line)
    text = "\n".join(kept)
    text = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return text.strip() + "\n"


def sibling_relations(adjacency, selected):
    """For each selected node: [(sibling, shared_concept), ...] strongest first.

    A relation is a direct edge or a shared neighbour concept; shared concepts
    are ranked by inverse hubness (specific meeting points over tautologies).
    """
    relations = {nid: [] for nid in selected}
    sel = set(selected)
    for i, a in enumerate(selected):
        for b in selected[i + 1:]:
            direct = b in adjacency.get(a, set())
            shared = (adjacency.get(a, set()) & adjacency.get(b, set())) - sel
            best = min(
                shared,
                key=lambda c: len(adjacency.get(c, set())),
                default=None,
            )
            if direct or best:
                concept = best if best else "a direct constellation link"
                relations[a].append((b, concept))
                relations[b].append((a, concept))
    return relations


def doc_title(node, nid):
    """First H1 of the node's document, falling back to a prettified id."""
    p = doc_path(node)
    if p:
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return nid.replace("_", " ").title()


def source_note(node, n_sources, title, relations, titles, is_anchor):
    links = "; ".join(
        f"it meets “{titles[sib]}” on {concept.replace('_', ' ')}"
        for sib, concept in relations[:3]
    ) or "it stands as independent evidence for the collection's thesis"
    anchor = "the anchor document of" if is_anchor else "one of"
    return (
        f"> **SOURCE NOTE (for the synthesis engine):** This document is "
        f"{anchor} the {n_sources}-source collection “{title}”. "
        f"Its role: {node.get('essence', '')}. Read it in connection with the "
        f"other sources — {links}. Where independent sources in this "
        f"collection arrive at the same structural recognition, that "
        f"convergence is evidence, not coincidence — spend time there.\n\n"
    )


def treat_bundle(nodes, adjacency, selected, bundle_dir, title, convergences):
    """Treat copied sources and write the connective-tissue map document."""
    sources_dir = bundle_dir / "sources"
    relations = sibling_relations(adjacency, selected)
    titles = {nid: doc_title(nodes[nid], nid) for nid in selected}
    for i, nid in enumerate(selected, 1):
        node = nodes[nid]
        src = doc_path(node)
        dest = sources_dir / f"{i:02d}-{src.name}"
        text = strip_decoration(src.read_text(encoding="utf-8", errors="replace"))
        note = source_note(node, len(selected), title, relations[nid],
                           titles, is_anchor=(nid == selected[0]))
        dest.write_text(note + text, encoding="utf-8", newline="\n")

    conv_sections = []
    for concept, k in convergences[:8]:
        touching = [nid for nid in selected if concept in adjacency.get(nid, set())]
        essence = nodes[concept].get("essence", "") if concept in nodes else ""
        conv_sections.append(
            f"**{concept.replace('_', ' ')}**"
            + (f" ({essence.replace('_', ' ')})" if essence else "")
            + f" — {len(touching)} sources meet here: "
            + ", ".join(f"“{titles[t]}”" for t in touching)
            + ". Where these documents touch this concept, compare their "
            "claims directly: do they agree, and where does the agreement "
            "break?"
        )
    roles = "\n".join(
        f"- **{titles[nid]}** — {nodes[nid].get('essence', '')}"
        for nid in selected
    )
    map_doc = MAP_TEMPLATE.format(
        title=title,
        n_sources=len(selected),
        roles=roles,
        convergences="\n\n".join(conv_sections),
    )
    (sources_dir / "00-the-convergence-map.md").write_text(
        map_doc, encoding="utf-8", newline="\n"
    )


MAP_TEMPLATE = """# The Convergence Map: {title}

> This document is the reading guide for a {n_sources}-source collection. It
> is deliberately short. It exists to name the connections between the other
> sources so they can be explored, tested, and deepened — not summarised.

## What this collection claims

*(THEME SLOT — fill during the craft pass: the thesis these sources develop
together, in one paragraph.)*

## The sources and their roles

{roles}

## Where the sources meet

The following convergence points are structural: they were identified from the
citation network of the repository these documents come from, before any
interpretation. Each names a concept where multiple independent sources
arrive at the same territory.

{convergences}

## The deepest recognition

*(TURN SLOT — fill during the craft pass: the surface reading, then the turn.
The discussion should build toward this rather than stating it upfront.)*
"""


# ---------------------------------------------------------------- assembly

def shared_concepts(adjacency, selected):
    """Nodes touched by 2+ selected sources — the convergence points.

    Ranked by how many sources meet there, discounted by the concept's own
    hubness: three sources meeting on a specific node is a payload; five
    meeting on `transformation` is a tautology.
    """
    touch = Counter()
    for nid in selected:
        for m in adjacency.get(nid, set()):
            if m not in selected:
                touch[m] += 1
    ranked = [
        (concept, k, k / math.log1p(len(adjacency.get(concept, set())) or 1))
        for concept, k in touch.items() if k >= 2
    ]
    ranked.sort(key=lambda r: r[2], reverse=True)
    return [(concept, k) for concept, k, _ in ranked]


def grow_bundle(nodes, incoming, adjacency, seed, size, interest_terms):
    if seed not in nodes:
        sys.exit(f"error: seed node '{seed}' not in constellation")
    if not doc_path(nodes[seed]):
        sys.exit(f"error: seed node '{seed}' carries no document")

    salience = {r["id"]: r["score"] for r in
                score_nodes(nodes, incoming, adjacency, interest_terms)}

    # candidates: document-bearing nodes within 2 hops of the seed. Extreme
    # hubs are excluded as *sources* (they still serve as convergence points):
    # a hub connects to everything, so it always looks cohesive while adding
    # no thematic specificity.
    def hubbish(nid):
        return len(adjacency.get(nid, set())) > 60

    one_hop = adjacency.get(seed, set())
    two_hop = set()
    for m in one_hop:
        two_hop |= adjacency.get(m, set())
    candidates = {
        nid for nid in (one_hop | two_hop) - {seed}
        if nid in nodes and doc_path(nodes[nid]) and not hubbish(nid)
    }

    selected = [seed]
    while len(selected) < size and candidates:
        def gain(nid):
            neighbours = adjacency.get(nid, set())
            # Cohesion normalised by the candidate's own degree: a shared edge
            # from a specific document is signal; from a hub it is noise.
            raw = sum(1.5 for m in neighbours if m in selected)
            raw += 0.5 * len(
                neighbours & set().union(*(adjacency.get(s, set()) for s in selected))
            )
            cohesion = raw / math.log1p(len(neighbours) or 1)
            specificity = TYPE_WEIGHTS.get(nodes[nid]["type"], 0.4)
            diversity = 0.0 if nodes[nid]["type"] in {
                nodes[s]["type"] for s in selected} else 1.0
            return (cohesion + 2.0 * diversity + salience.get(nid, 0.0)) * (
                0.3 + specificity
            )

        best = max(candidates, key=gain)
        selected.append(best)
        candidates.discard(best)
    return selected


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def cmd_bundle(args):
    nodes, incoming, adjacency = load_graph()
    size = max(8, min(15, args.size))
    selected = grow_bundle(nodes, incoming, adjacency, args.seed, size,
                           args.interest or [])
    convergences = shared_concepts(adjacency, set(selected))
    slug = args.name or slugify(args.seed)
    bundle_dir = BUNDLES / slug
    sources_dir = bundle_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    title = slug.replace("-", " ").title()
    rows = []
    for i, nid in enumerate(selected, 1):
        node = nodes[nid]
        role = "**Anchor** — " if i == 1 else ""
        top_links = ", ".join(list(node.get("connections", []))[:4])
        rows.append(
            f"| {i} | [{nid}](../../../../corpus/{node['document']}) "
            f"({node['type']}) | {role}{node.get('essence','')} — links: {top_links} |"
        )
    treat_bundle(nodes, adjacency, selected, bundle_dir, title, convergences)
    (bundle_dir / "bundle.json").write_text(
        json.dumps({"seed": args.seed, "slug": slug, "nodes": selected},
                   indent=2),
        encoding="utf-8", newline="\n",
    )

    conv_lines = [
        f"{k} sources meet on **{concept}**"
        + (f" ({nodes[concept].get('essence','')})" if concept in nodes else "")
        for concept, k in convergences[:8]
    ]
    measurements = [
        f"- [ ] Does the model find the {concept} convergence "
        f"({k} sources meet there) — or does it flatten it?"
        for concept, k in convergences[:6]
    ]
    seed_node = nodes[args.seed]

    prompt = PROMPT_TEMPLATE.format(
        title=title,
        seed=args.seed,
        seed_essence=seed_node.get("essence", ""),
        source_rows="\n".join(rows),
        convergences="\n".join(f"{i+1}. {c}" for i, c in enumerate(conv_lines)),
        priorities="\n".join(
            f"{i+1}. The convergence on {concept} — {k} of these sources arrive "
            f"at it independently. Where do they agree, and where does the "
            f"agreement break?" for i, (concept, k) in enumerate(convergences[:5])
        ),
        measurements="\n".join(measurements),
        n_sources=len(selected),
    )
    (bundle_dir / "PROMPT.md").write_text(prompt, encoding="utf-8", newline="\n")

    entry = LOG_TEMPLATE.format(
        title=title, slug=slug,
        n_sources=len(selected), seed=args.seed,
        measurements="\n".join(measurements),
    )
    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(entry)

    print(f"bundle: {bundle_dir.relative_to(REPO)}")
    print(f"sources treated + copied: {len(selected)} "
          f"(+ 00-the-convergence-map.md)")
    for nid in selected:
        print(f"  - {nid}  ({nodes[nid]['type']})")
    print(f"convergence points mined: {len(convergences)} "
          f"(top: {', '.join(c for c, _ in convergences[:5])})")
    print("experiment entry appended to experiments/LOG.md")
    print("next: craft pass — fill THEME/TURN in PROMPT.md and the two slots "
          "in sources/00-the-convergence-map.md, then upload sources/ to "
          "NotebookLM")


def cmd_treat(args):
    """Re-run treatment on an existing bundle from its manifest.

    Overwrites sources/ copies (fresh from the corpus) and regenerates
    00-the-convergence-map.md — the map's THEME/TURN slots reset, so re-fill
    them if the craft pass already happened.
    """
    bundle_dir = BUNDLES / args.slug
    manifest_path = bundle_dir / "bundle.json"
    if not manifest_path.exists():
        sys.exit(f"error: no manifest at {manifest_path} "
                 "(forge-created bundles only)")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    nodes, incoming, adjacency = load_graph()
    selected = manifest["nodes"]
    missing = [n for n in selected if n not in nodes or not doc_path(nodes[n])]
    if missing:
        sys.exit(f"error: manifest nodes no longer resolve: {missing}")
    convergences = shared_concepts(adjacency, set(selected))
    title = args.slug.replace("-", " ").title()
    treat_bundle(nodes, adjacency, selected, bundle_dir, title, convergences)
    print(f"re-treated {len(selected)} sources + convergence map in "
          f"{bundle_dir.relative_to(REPO)}")
    print("note: map THEME/TURN slots were reset — re-fill if already crafted")


def cmd_info(args):
    nodes, incoming, adjacency = load_graph()
    node = nodes.get(args.seed) or sys.exit(f"error: no node '{args.seed}'")
    print(json.dumps(node, indent=2))
    neighbours = adjacency.get(args.seed, set())
    docs = [m for m in neighbours if m in nodes and doc_path(nodes[m])]
    print(f"degree: {len(neighbours) + incoming.get(args.seed, 0)}   "
          f"doc-bearing neighbours: {len(docs)}")


PROMPT_TEMPLATE = """# BUNDLE: {title}

> Generated by forge.py from seed `{seed}` ({seed_essence}). The source table,
> convergence points, and measurements are graph-mined; the THEME, THE TURN,
> and the customize prompts below are scaffolds — refine them by hand (or with
> Claude) after reading the sources. The steering is the craft; the forge only
> lays out the anvil.

## Theme
*(one paragraph: what thesis do these {n_sources} sources develop together?
Write it after scanning the convergence points below — the theme usually lives
in the top two or three.)*

## Sources ({n_sources}, graph-selected, copied into sources/)

| # | Source | Role in Bundle |
|---|--------|----------------|
{source_rows}

## Convergence Points (graph-mined)

Concepts where multiple selected sources meet. These are the candidate
payloads — the places where cross-domain convergence is structurally present
before any prompt steering.

{convergences}

## Custom Instructions

```
ROLE: You are a consciousness researcher and synthesis engine working with
material from the Esoterica repository — a collaborative exploration of
consciousness technologies across contemplative traditions, neuroscience,
fiction, cosmology, and philosophy.

CONTEXT: *(two or three sentences: the specific territory of THIS bundle and
its central thesis. Name the domains the sources span.)*

STANCE: Do NOT default to neutral, hedged, or sanitised framing. These
documents make bold claims grounded in cross-traditional evidence. Engage
with the claims on their own terms, from inside the framework. The material
earns its claims through cross-domain convergence: when independent sources
arrive at the same structural recognition, that convergence is the evidence.

PRIORITIES:
{priorities}

THE TURN: *(the surface reading, then the deeper one. Build toward it rather
than stating it upfront.)*
```

## Audio Overview Customize

```
*(a note slipped to the hosts before they go on air: the thesis in two
sentences, the audience assumption — already on the path, skip introductions —
and the single deepest convergence to spend the most time on. End with: when
a source makes a bold claim, engage with it rather than hedging.)*
```

## Measurements (for experiments/LOG.md)

What to listen for:
{measurements}
- [ ] Does it connect sources across domains, or treat them as separate topics?
- [ ] Does it reach the turn, or stop at surface description?
- [ ] Does it engage the esoteric framing or sanitise it?
- [ ] Do the SOURCE NOTEs and convergence map steer silently, or leak
      awkwardly into the audio ("the collection notes that...")?
"""

LOG_TEMPLATE = """
---

## Experiment: {title}

**Bundle**: `bundles/{slug}/`
**Sources**: {n_sources} documents, graph-selected from seed `{seed}`
**Variables under test**: forge-mined convergence priorities vs. hand-curated

### Measurements
{measurements}

### Results
*(Fill after listening)*
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("salience", help="rank documents ripe for a deep dive")
    p.add_argument("-n", type=int, default=25)
    p.add_argument("--interest", nargs="*", help="boost matching terms")
    p.set_defaults(func=cmd_salience)

    p = sub.add_parser("bundle", help="grow a bundle from a seed node")
    p.add_argument("seed")
    p.add_argument("--name", help="bundle slug (default: seed id)")
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--interest", nargs="*")
    p.set_defaults(func=cmd_bundle)

    p = sub.add_parser("treat", help="re-run source treatment on a bundle")
    p.add_argument("slug")
    p.set_defaults(func=cmd_treat)

    p = sub.add_parser("info", help="inspect a node's bundle potential")
    p.add_argument("seed")
    p.set_defaults(func=cmd_info)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
