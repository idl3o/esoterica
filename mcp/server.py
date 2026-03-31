"""
Esoterica MCP Server v2 — Living Constellation Interface

Exposes the esoterica repository's knowledge graph, document network,
and consciousness technologies as tools, resources, and prompts for
any MCP-compatible client.

Run:
    python server.py              # stdio mode (for Claude Code / Claude Desktop)
    python server.py --http 8080  # HTTP mode (for remote clients)

Requires:
    pip install mcp
"""

import json
import math
import os
import random
import re
import sys
from collections import Counter
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
CONSTELLATION_PATH = REPO_ROOT / "constellation" / "constellation.json"

SEARCH_DIRS = [
    "distillations", "synthesis", "fiction-bridges", "protocols",
    "seeds", "traditions", "translated", "extractions",
    "correspondences", "garden", "journey",
]

# ---------------------------------------------------------------------------
# TF-IDF engine (stdlib only)
# ---------------------------------------------------------------------------

_TOKENIZE_RE = re.compile(r"[a-z0-9]{3,}", re.ASCII)


def _tokenize(text: str) -> list[str]:
    return _TOKENIZE_RE.findall(text.lower())


@dataclass
class TFIDFIndex:
    doc_paths: list[str] = field(default_factory=list)
    doc_titles: list[str] = field(default_factory=list)
    doc_previews: list[str] = field(default_factory=list)
    idf: dict[str, float] = field(default_factory=dict)
    tf_vectors: list[dict[str, float]] = field(default_factory=list)

    def query(self, text: str, max_results: int = 10,
              filter_dirs: list[str] | None = None) -> list[dict]:
        tokens = _tokenize(text)
        if not tokens:
            return []
        scores: list[tuple[float, int]] = []
        for i, tf in enumerate(self.tf_vectors):
            if filter_dirs:
                if not any(self.doc_paths[i].startswith(d) for d in filter_dirs):
                    continue
            score = sum(tf.get(t, 0.0) * self.idf.get(t, 0.0) for t in tokens)
            if score > 0:
                scores.append((score, i))
        scores.sort(key=lambda x: -x[0])
        results = []
        for score, i in scores[:max_results]:
            results.append({
                "path": self.doc_paths[i],
                "title": self.doc_titles[i],
                "preview": self.doc_previews[i],
                "score": round(score, 4),
            })
        return results


def _build_tfidf(repo_root: Path, dirs: list[str]) -> TFIDFIndex:
    idx = TFIDFIndex()
    doc_tokens: list[list[str]] = []
    df: Counter = Counter()

    for d in dirs:
        dp = repo_root / d
        if not dp.exists():
            continue
        for md in dp.rglob("*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            title = md.stem
            for line in text.splitlines()[:20]:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            tokens = _tokenize(text)
            idx.doc_paths.append(str(md.relative_to(repo_root)))
            idx.doc_titles.append(title)
            idx.doc_previews.append(text[:300].strip())
            doc_tokens.append(tokens)
            df.update(set(tokens))

    n = len(idx.doc_paths)
    if n == 0:
        return idx

    idx.idf = {t: math.log(n / c) for t, c in df.items()}
    for tokens in doc_tokens:
        total = len(tokens) or 1
        tf = Counter(tokens)
        idx.tf_vectors.append({t: c / total for t, c in tf.items()})

    return idx


# ---------------------------------------------------------------------------
# State object
# ---------------------------------------------------------------------------

@dataclass
class ConstellationState:
    data: dict
    mtime: float
    type_index: dict[str, list[str]] = field(default_factory=dict)
    essence_index: dict[str, list[str]] = field(default_factory=dict)
    reverse_connections: dict[str, list[str]] = field(default_factory=dict)
    doc_index: dict[str, str] = field(default_factory=dict)
    tfidf: TFIDFIndex | None = None


def _load_constellation() -> dict:
    """Load constellation.json, repairing brace mismatches."""
    text = CONSTELLATION_PATH.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        opens = text.count("{")
        closes = text.count("}")
        if closes > opens:
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                pos = e.pos
                check = pos - 1
                while check >= 0 and text[check] in " \t\n\r":
                    check -= 1
                if text[check] == "}":
                    fixed = text[:check] + " " + text[check + 1:]
                    try:
                        data = json.loads(fixed)
                    except json.JSONDecodeError:
                        data = _parse_nodes_only(text)
                else:
                    data = _parse_nodes_only(text)
        else:
            data = _parse_nodes_only(text)

    # Merge stray node-shaped entries into nodes
    merged_nodes = dict(data.get("nodes", {}))
    node_keys = {"type", "essence", "connections"}
    for key, value in data.items():
        if key == "nodes":
            continue
        if isinstance(value, dict) and node_keys.issubset(value.keys()):
            merged_nodes[key] = value

    return {"nodes": merged_nodes}


def _parse_nodes_only(text: str) -> dict:
    match = re.search(r'"nodes"\s*:\s*\{', text)
    if not match:
        return {"nodes": {}}
    depth = 0
    start = match.end() - 1
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return {"nodes": json.loads(text[start: i + 1])}
    return {"nodes": {}}


def _build_indexes(state: ConstellationState):
    state.type_index = {}
    state.essence_index = {}
    state.reverse_connections = {}
    state.doc_index = {}
    all_nodes = state.data.get("nodes", {})

    for node_id, data in all_nodes.items():
        t = data.get("type", "unknown")
        state.type_index.setdefault(t, []).append(node_id)
        e = data.get("essence", "")
        if e:
            state.essence_index.setdefault(e, []).append(node_id)
        for conn in data.get("connections", []):
            state.reverse_connections.setdefault(conn, []).append(node_id)
        doc = data.get("document", "")
        if doc:
            state.doc_index[node_id] = doc


def _build_state(mtime: float, build_tfidf: bool = True) -> ConstellationState:
    data = _load_constellation()
    state = ConstellationState(data=data, mtime=mtime)
    _build_indexes(state)
    if build_tfidf:
        state.tfidf = _build_tfidf(REPO_ROOT, SEARCH_DIRS)
    return state


_state: ConstellationState | None = None


def _ensure_state() -> ConstellationState:
    global _state
    current_mtime = CONSTELLATION_PATH.stat().st_mtime
    if _state is None or current_mtime != _state.mtime:
        _state = _build_state(current_mtime)
    return _state


def _persist_constellation():
    """Write current state to disk and rebuild indexes."""
    global _state
    text = json.dumps(_state.data, indent=4, ensure_ascii=False)
    CONSTELLATION_PATH.write_text(text, encoding="utf-8")
    _state.mtime = CONSTELLATION_PATH.stat().st_mtime
    _build_indexes(_state)


# ---------------------------------------------------------------------------
# Document layer
# ---------------------------------------------------------------------------

def _read_document(rel_path: str, max_lines: int = 100) -> str | None:
    full = REPO_ROOT / rel_path
    if not full.exists():
        return None
    lines = full.read_text(encoding="utf-8", errors="replace").splitlines()
    text = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        text += f"\n\n... ({len(lines) - max_lines} more lines)"
    return text


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(server: FastMCP):
    global _state
    mtime = CONSTELLATION_PATH.stat().st_mtime
    _state = _build_state(mtime)
    n = len(_state.data.get("nodes", {}))
    t = len(_state.tfidf.doc_paths) if _state.tfidf else 0
    print(f"Esoterica MCP server ready — {n} nodes, {t} documents indexed",
          file=sys.stderr)
    yield {}


mcp = FastMCP(
    "esoterica",
    instructions="Navigate the esoterica consciousness technology repository — "
                 "constellation graph, document network, and knowledge synthesis.",
    lifespan=lifespan,
)


# ===================================================================
# TOOLS — Constellation Navigation (existing, refactored)
# ===================================================================

@mcp.tool()
def get_node(node_id: str) -> dict[str, Any]:
    """
    Get a constellation node by ID.

    Returns the node's type, essence, connections, document link,
    description, and which other nodes connect back to it.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    n = all_nodes.get(node_id)
    if n is None:
        matches = [k for k in all_nodes if node_id.lower() in k.lower()]
        if matches:
            return {"error": f"Node '{node_id}' not found", "similar": matches[:10]}
        return {"error": f"Node '{node_id}' not found"}
    result = {"id": node_id, **n}
    result["referenced_by"] = state.reverse_connections.get(node_id, [])
    return result


@mcp.tool()
def traverse(start: str, depth: int = 1) -> dict[str, Any]:
    """
    Traverse the constellation from a starting node.

    Returns all nodes reachable within `depth` hops, with their
    connections. Depth 1 = direct neighbors. Depth 2 = neighbors
    of neighbors. Max depth 3 to keep results manageable.
    """
    depth = min(depth, 3)
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if start not in all_nodes:
        matches = [k for k in all_nodes if start.lower() in k.lower()]
        return {"error": f"Node '{start}' not found", "similar": matches[:10]}

    visited = {start}
    frontier = {start}
    layers = []

    for d in range(depth):
        next_frontier = set()
        for node_id in frontier:
            node = all_nodes.get(node_id, {})
            for conn in node.get("connections", []):
                if conn not in visited and conn in all_nodes:
                    next_frontier.add(conn)
            for ref in state.reverse_connections.get(node_id, []):
                if ref not in visited and ref in all_nodes:
                    next_frontier.add(ref)
        visited.update(next_frontier)
        if next_frontier:
            layers.append({"depth": d + 1, "nodes": sorted(next_frontier)})
        frontier = next_frontier

    summaries = {}
    for nid in visited:
        n = all_nodes.get(nid, {})
        summaries[nid] = {
            "type": n.get("type", "?"),
            "essence": n.get("essence", "?"),
            "connections_count": len(n.get("connections", [])),
        }
    return {
        "center": start,
        "total_reached": len(visited),
        "layers": layers,
        "summaries": summaries,
    }


@mcp.tool()
def find_path(source: str, target: str) -> dict[str, Any]:
    """
    Find the shortest connection path between two constellation nodes.

    Uses bidirectional BFS over the connection graph (treating all
    links as undirected). Returns the path and each node's summary.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    for name, label in [(source, "source"), (target, "target")]:
        if name not in all_nodes:
            matches = [k for k in all_nodes if name.lower() in k.lower()]
            return {"error": f"{label} '{name}' not found", "similar": matches[:10]}

    adj: dict[str, set[str]] = {}
    for nid, data in all_nodes.items():
        adj.setdefault(nid, set())
        for conn in data.get("connections", []):
            if conn in all_nodes:
                adj.setdefault(nid, set()).add(conn)
                adj.setdefault(conn, set()).add(nid)

    queue = [(source, [source])]
    seen = {source}
    while queue:
        current, path = queue.pop(0)
        if current == target:
            path_details = []
            for nid in path:
                n = all_nodes.get(nid, {})
                path_details.append({
                    "id": nid,
                    "type": n.get("type"),
                    "essence": n.get("essence"),
                })
            return {
                "connected": True,
                "distance": len(path) - 1,
                "path": [p["id"] for p in path_details],
                "details": path_details,
            }
        for neighbor in adj.get(current, set()):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return {"connected": False, "source": source, "target": target}


@mcp.tool()
def list_types() -> dict[str, int]:
    """List all node types in the constellation with their counts."""
    state = _ensure_state()
    return {k: len(v) for k, v in sorted(state.type_index.items(), key=lambda x: -len(x[1]))}


@mcp.tool()
def nodes_by_type(node_type: str) -> list[dict[str, str]]:
    """
    Get all constellation nodes of a given type.

    Common types: archetype, element, cosmological, architecture,
    practice, tradition, fiction_bridge, translation, seed, etc.
    """
    state = _ensure_state()
    ids = state.type_index.get(node_type, [])
    if not ids:
        return [{"error": f"No nodes of type '{node_type}'",
                 "available_types": list(state.type_index.keys())}]
    all_nodes = state.data.get("nodes", {})
    result = []
    for nid in sorted(ids):
        n = all_nodes.get(nid, {})
        result.append({
            "id": nid,
            "essence": n.get("essence", ""),
            "connections_count": len(n.get("connections", [])),
            "has_document": bool(n.get("document")),
        })
    return result


@mcp.tool()
def search_constellation(query: str, max_results: int = 15) -> list[dict]:
    """
    Search constellation nodes by ID, essence, type, description,
    or connection names. Weighted scoring with fuzzy substring matching.
    """
    state = _ensure_state()
    query_lower = query.lower()
    results = []

    for nid, data in state.data.get("nodes", {}).items():
        score = 0
        # ID exact match is strongest signal
        if query_lower == nid.lower():
            score += 10
        elif query_lower in nid.lower():
            score += 3
        if query_lower in data.get("essence", "").lower():
            score += 2
        desc = data.get("description", "")
        if query_lower in desc.lower():
            score += 2
        if query_lower in data.get("type", "").lower():
            score += 1
        if any(query_lower in c.lower() for c in data.get("connections", [])):
            score += 1

        if score > 0:
            # Build snippet from description
            snippet = ""
            if desc:
                idx = desc.lower().find(query_lower)
                if idx >= 0:
                    start = max(0, idx - 50)
                    end = min(len(desc), idx + len(query_lower) + 50)
                    snippet = ("..." if start > 0 else "") + desc[start:end] + ("..." if end < len(desc) else "")
                else:
                    snippet = desc[:120]
            results.append({
                "id": nid,
                "type": data.get("type"),
                "essence": data.get("essence"),
                "score": score,
                "has_document": bool(data.get("document")),
                "snippet": snippet,
            })

    results.sort(key=lambda x: -x["score"])
    return results[:max_results]


@mcp.tool()
def read_document(node_id: str, max_lines: int = 150) -> dict[str, Any]:
    """
    Read the document linked to a constellation node.

    Returns the document content (first max_lines lines) if the node
    has a document path. Use this to go deeper on any node.
    """
    state = _ensure_state()
    doc_path = state.doc_index.get(node_id)
    if not doc_path:
        all_nodes = state.data.get("nodes", {})
        n = all_nodes.get(node_id)
        if n and "document" in n:
            doc_path = n["document"]
        else:
            return {"error": f"No document linked to node '{node_id}'"}

    content = _read_document(doc_path, max_lines)
    if content is None:
        return {"error": f"Document not found: {doc_path}"}
    return {"node_id": node_id, "path": doc_path, "content": content}


@mcp.tool()
def search_documents(query: str, directories: list[str] | None = None,
                     max_results: int = 10, use_tfidf: bool = True) -> list[dict]:
    """
    Full-text search across repository documents.

    Searches markdown files for the query string. When use_tfidf is True
    (default), results are ranked by TF-IDF relevance. Set use_tfidf=False
    for simple substring matching. Optionally filter by directory
    (e.g. ["distillations", "fiction-bridges"]).
    """
    state = _ensure_state()
    if use_tfidf and state.tfidf and state.tfidf.doc_paths:
        return state.tfidf.query(query, max_results, directories)
    # Fallback: substring search
    query_lower = query.lower()
    dirs = directories or SEARCH_DIRS
    results = []
    for d in dirs:
        dir_path = REPO_ROOT / d
        if not dir_path.exists():
            continue
        for md in dir_path.rglob("*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if query_lower in text.lower():
                title = md.stem
                for line in text.splitlines()[:20]:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                results.append({
                    "path": str(md.relative_to(REPO_ROOT)),
                    "title": title,
                    "preview": text[:300].strip(),
                })
                if len(results) >= max_results:
                    return results
    return results


@mcp.tool()
def repository_overview() -> dict[str, Any]:
    """
    Get an overview of the esoterica repository — node counts by type,
    total documents, directory sizes, and constellation stats.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    type_counts = {k: len(v) for k, v in
                   sorted(state.type_index.items(), key=lambda x: -len(x[1]))}
    total_connections = sum(
        len(n.get("connections", [])) for n in all_nodes.values()
    )
    dir_counts = {}
    for d in SEARCH_DIRS:
        p = REPO_ROOT / d
        if p.exists():
            dir_counts[d] = len(list(p.rglob("*.md")))
    return {
        "constellation": {
            "total_nodes": len(all_nodes),
            "types": type_counts,
            "total_connections": total_connections,
            "nodes_with_documents": len(state.doc_index),
        },
        "directories": dir_counts,
        "total_markdown_files": sum(dir_counts.values()),
    }


@mcp.tool()
def find_connections_between(concept_a: str, concept_b: str) -> dict[str, Any]:
    """
    Find how two concepts are connected in the constellation.

    Returns the shortest path, shared connections, and common neighbors.
    Useful for discovering unexpected bridges between ideas.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    matches_a = [k for k in all_nodes if concept_a.lower() in k.lower()]
    matches_b = [k for k in all_nodes if concept_b.lower() in k.lower()]

    if not matches_a:
        return {"error": f"No nodes matching '{concept_a}'"}
    if not matches_b:
        return {"error": f"No nodes matching '{concept_b}'"}

    node_a = matches_a[0]
    node_b = matches_b[0]
    conns_a = set(all_nodes.get(node_a, {}).get("connections", []))
    conns_b = set(all_nodes.get(node_b, {}).get("connections", []))
    shared = conns_a & conns_b
    path_result = find_path(node_a, node_b)

    return {
        "node_a": node_a,
        "node_b": node_b,
        "shared_connections": sorted(shared),
        "path": path_result,
        "connections_a_only": sorted(conns_a - conns_b)[:15],
        "connections_b_only": sorted(conns_b - conns_a)[:15],
    }


@mcp.tool()
def nearby_technologies(seed_concept: str, depth: int = 2) -> list[dict]:
    """
    Find consciousness technologies near a concept.

    Traverses from the seed concept and returns nodes that have
    linked documents (i.e., developed technologies, not just
    abstract nodes). Ordered by proximity.
    """
    traversal = traverse(seed_concept, depth=depth)
    if "error" in traversal:
        return [traversal]

    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    technologies = []

    for layer in traversal.get("layers", []):
        for nid in layer["nodes"]:
            n = all_nodes.get(nid, {})
            if n.get("document"):
                technologies.append({
                    "id": nid,
                    "type": n.get("type"),
                    "essence": n.get("essence"),
                    "document": n.get("document"),
                    "depth": layer["depth"],
                    "description": (n.get("description", ""))[:200],
                })

    center = all_nodes.get(traversal["center"], {})
    if center.get("document"):
        technologies.insert(0, {
            "id": traversal["center"],
            "type": center.get("type"),
            "essence": center.get("essence"),
            "document": center.get("document"),
            "depth": 0,
            "description": (center.get("description", ""))[:200],
        })

    return technologies


# ===================================================================
# TOOLS — Write (new)
# ===================================================================

@mcp.tool()
def add_node(
    node_id: str,
    type: str,
    essence: str,
    connections: list[str] | None = None,
    description: str | None = None,
    document: str | None = None,
) -> dict[str, Any]:
    """
    Add a new node to the constellation.

    Creates a node with the given ID, type, essence, and optional
    connections, description, and document path. Persists to disk.
    Rejects duplicate IDs. Warns if connections reference non-existent nodes.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if node_id in all_nodes:
        return {"error": f"Node '{node_id}' already exists. Use update_node to modify."}

    node: dict[str, Any] = {
        "type": type,
        "essence": essence,
        "connections": connections or [],
    }
    if description:
        node["description"] = description
    if document:
        node["document"] = document

    # Warn about dangling connections
    dangling = [c for c in node["connections"] if c not in all_nodes]

    all_nodes[node_id] = node
    _persist_constellation()

    result: dict[str, Any] = {"created": node_id, "node": node}
    if dangling:
        result["warnings"] = [f"Connection target '{c}' does not exist" for c in dangling]
    return result


@mcp.tool()
def update_node(
    node_id: str,
    type: str | None = None,
    essence: str | None = None,
    connections: list[str] | None = None,
    description: str | None = None,
    document: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing constellation node.

    Only fields that are provided (non-None) will be updated.
    Persists changes to disk immediately.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if node_id not in all_nodes:
        matches = [k for k in all_nodes if node_id.lower() in k.lower()]
        return {"error": f"Node '{node_id}' not found",
                **({"similar": matches[:10]} if matches else {})}

    node = all_nodes[node_id]
    updated = []
    if type is not None:
        node["type"] = type
        updated.append("type")
    if essence is not None:
        node["essence"] = essence
        updated.append("essence")
    if connections is not None:
        node["connections"] = connections
        updated.append("connections")
    if description is not None:
        node["description"] = description
        updated.append("description")
    if document is not None:
        node["document"] = document
        updated.append("document")

    _persist_constellation()
    return {"updated": node_id, "fields_changed": updated, "node": node}


@mcp.tool()
def add_connection(source: str, target: str, bidirectional: bool = True) -> dict[str, Any]:
    """
    Add a connection between two constellation nodes.

    By default adds the connection in both directions. Set
    bidirectional=False for a one-way link. Deduplicates.
    Both nodes must exist.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    for name, label in [(source, "source"), (target, "target")]:
        if name not in all_nodes:
            return {"error": f"{label} node '{name}' not found"}

    added = []
    if target not in all_nodes[source].get("connections", []):
        all_nodes[source].setdefault("connections", []).append(target)
        added.append(f"{source} → {target}")
    if bidirectional and source not in all_nodes[target].get("connections", []):
        all_nodes[target].setdefault("connections", []).append(source)
        added.append(f"{target} → {source}")

    if added:
        _persist_constellation()
    return {"added": added, "already_existed": not added}


@mcp.tool()
def remove_node(node_id: str) -> dict[str, Any]:
    """
    Remove a node from the constellation.

    Also removes all references to this node from other nodes'
    connection lists. Persists to disk.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if node_id not in all_nodes:
        return {"error": f"Node '{node_id}' not found"}

    removed_node = all_nodes.pop(node_id)
    # Clean dangling references
    cleaned_from = []
    for nid, data in all_nodes.items():
        conns = data.get("connections", [])
        if node_id in conns:
            conns.remove(node_id)
            cleaned_from.append(nid)

    _persist_constellation()
    return {
        "removed": node_id,
        "had_connections": removed_node.get("connections", []),
        "cleaned_references_from": cleaned_from,
    }


# ===================================================================
# TOOLS — Graph Analytics (new)
# ===================================================================

@mcp.tool()
def graph_stats() -> dict[str, Any]:
    """
    Get structural statistics about the constellation graph.

    Returns total nodes/edges, degree distribution, most/least connected
    nodes, orphan count, and sampled clustering coefficient.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    # Build undirected adjacency for clustering
    adj: dict[str, set[str]] = {}
    for nid, data in all_nodes.items():
        adj.setdefault(nid, set())
        for conn in data.get("connections", []):
            if conn in all_nodes:
                adj[nid].add(conn)
                adj.setdefault(conn, set()).add(nid)

    degrees = {nid: len(neighbors) for nid, neighbors in adj.items()}
    total_directed = sum(len(n.get("connections", [])) for n in all_nodes.values())
    total_undirected = sum(degrees.values()) // 2
    orphans = [nid for nid, deg in degrees.items() if deg == 0]

    # Degree distribution buckets
    buckets = {"0": 0, "1-5": 0, "6-10": 0, "11-20": 0, "21-50": 0, "51+": 0}
    for deg in degrees.values():
        if deg == 0:
            buckets["0"] += 1
        elif deg <= 5:
            buckets["1-5"] += 1
        elif deg <= 10:
            buckets["6-10"] += 1
        elif deg <= 20:
            buckets["11-20"] += 1
        elif deg <= 50:
            buckets["21-50"] += 1
        else:
            buckets["51+"] += 1

    # Top and bottom nodes by degree
    sorted_degrees = sorted(degrees.items(), key=lambda x: -x[1])
    top_10 = [{"id": nid, "degree": deg} for nid, deg in sorted_degrees[:10]]

    # Sampled clustering coefficient
    sample_size = min(100, len(all_nodes))
    sample_nodes = random.sample(list(adj.keys()), sample_size) if adj else []
    cc_sum = 0.0
    cc_count = 0
    for nid in sample_nodes:
        neighbors = list(adj[nid])
        k = len(neighbors)
        if k < 2:
            continue
        links = 0
        for i in range(k):
            for j in range(i + 1, k):
                if neighbors[j] in adj.get(neighbors[i], set()):
                    links += 1
        cc_sum += (2 * links) / (k * (k - 1))
        cc_count += 1

    avg_cc = round(cc_sum / cc_count, 4) if cc_count > 0 else 0.0
    avg_degree = round(sum(degrees.values()) / len(degrees), 2) if degrees else 0

    return {
        "total_nodes": len(all_nodes),
        "total_directed_edges": total_directed,
        "total_undirected_edges": total_undirected,
        "average_degree": avg_degree,
        "max_degree": sorted_degrees[0] if sorted_degrees else None,
        "orphan_count": len(orphans),
        "degree_distribution": buckets,
        "most_connected": top_10,
        "clustering_coefficient": avg_cc,
        "clustering_sample_size": cc_count,
    }


@mcp.tool()
def find_clusters(min_size: int = 2) -> dict[str, Any]:
    """
    Find connected components in the constellation graph.

    Uses BFS over undirected edges. Returns clusters with their
    size, member nodes, and dominant type. Filtered by min_size.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    adj: dict[str, set[str]] = {}
    for nid, data in all_nodes.items():
        adj.setdefault(nid, set())
        for conn in data.get("connections", []):
            if conn in all_nodes:
                adj[nid].add(conn)
                adj.setdefault(conn, set()).add(nid)

    visited: set[str] = set()
    clusters = []

    for nid in all_nodes:
        if nid in visited:
            continue
        # BFS
        component = []
        queue = [nid]
        visited.add(nid)
        while queue:
            current = queue.pop(0)
            component.append(current)
            for neighbor in adj.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        if len(component) >= min_size:
            type_counts = Counter(
                all_nodes.get(n, {}).get("type", "unknown") for n in component
            )
            clusters.append({
                "size": len(component),
                "dominant_type": type_counts.most_common(1)[0] if type_counts else None,
                "members": sorted(component) if len(component) <= 50 else sorted(component)[:50] + [f"... and {len(component) - 50} more"],
            })

    clusters.sort(key=lambda x: -x["size"])
    return {
        "total_clusters": len(clusters),
        "clusters": clusters[:20],
    }


@mcp.tool()
def orphan_nodes() -> list[dict]:
    """
    Find nodes with no connections in or out.

    Returns nodes that have zero outgoing connections AND are not
    referenced by any other node's connection list.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    orphans = []
    for nid, data in all_nodes.items():
        out = len(data.get("connections", []))
        inc = len(state.reverse_connections.get(nid, []))
        if out == 0 and inc == 0:
            orphans.append({
                "id": nid,
                "type": data.get("type"),
                "essence": data.get("essence"),
            })
    return orphans


@mcp.tool()
def most_connected(n: int = 10) -> list[dict]:
    """
    Get the N most connected nodes in the constellation.

    Ranked by total degree (outgoing + incoming connections).
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    scored = []
    for nid, data in all_nodes.items():
        out_deg = len(data.get("connections", []))
        in_deg = len(state.reverse_connections.get(nid, []))
        scored.append({
            "id": nid,
            "type": data.get("type"),
            "essence": data.get("essence"),
            "out_degree": out_deg,
            "in_degree": in_deg,
            "total_degree": out_deg + in_deg,
        })
    scored.sort(key=lambda x: -x["total_degree"])
    return scored[:n]


# ===================================================================
# TOOLS — Serendipity (new)
# ===================================================================

@mcp.tool()
def random_node(type_filter: str | None = None) -> dict[str, Any]:
    """
    Get a random constellation node.

    Optionally filter by type (e.g. "archetype", "consciousness_technology").
    Returns the full node data with reverse connections.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if type_filter:
        candidates = state.type_index.get(type_filter, [])
        if not candidates:
            return {"error": f"No nodes of type '{type_filter}'",
                    "available_types": list(state.type_index.keys())}
    else:
        candidates = list(all_nodes.keys())

    chosen = random.choice(candidates)
    n = all_nodes[chosen]
    return {
        "id": chosen,
        **n,
        "referenced_by": state.reverse_connections.get(chosen, []),
    }


@mcp.tool()
def random_walk(start: str, steps: int = 5) -> dict[str, Any]:
    """
    Take a random walk through the constellation.

    From the starting node, randomly follow connections (forward or
    reverse) for the given number of steps. Max 10 steps.
    Returns the path taken.
    """
    steps = min(steps, 10)
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    if start not in all_nodes:
        matches = [k for k in all_nodes if start.lower() in k.lower()]
        return {"error": f"Node '{start}' not found",
                **({"similar": matches[:10]} if matches else {})}

    path = [start]
    current = start
    for _ in range(steps):
        n = all_nodes.get(current, {})
        forward = [c for c in n.get("connections", []) if c in all_nodes]
        reverse = [r for r in state.reverse_connections.get(current, []) if r in all_nodes]
        neighbors = list(set(forward + reverse) - set(path))
        if not neighbors:
            break
        current = random.choice(neighbors)
        path.append(current)

    walk = []
    for nid in path:
        n = all_nodes.get(nid, {})
        walk.append({
            "id": nid,
            "type": n.get("type"),
            "essence": n.get("essence"),
        })

    return {
        "steps_taken": len(path) - 1,
        "hit_dead_end": len(path) - 1 < steps,
        "path": walk,
    }


@mcp.tool()
def surprise_me() -> dict[str, Any]:
    """
    Get a serendipitous constellation discovery.

    Weighted random selection: nodes with documents get 5x weight,
    nodes with descriptions get 2x weight. Includes a document
    preview if available.
    """
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})

    weighted: list[tuple[str, int]] = []
    for nid, data in all_nodes.items():
        w = 1
        if data.get("document"):
            w = 5
        elif data.get("description"):
            w = 2
        weighted.append((nid, w))

    total = sum(w for _, w in weighted)
    r = random.randint(1, total)
    cumulative = 0
    chosen = weighted[0][0]
    for nid, w in weighted:
        cumulative += w
        if r <= cumulative:
            chosen = nid
            break

    n = all_nodes[chosen]
    result: dict[str, Any] = {
        "id": chosen,
        **n,
        "referenced_by": state.reverse_connections.get(chosen, []),
    }

    # Include document preview if available
    doc_path = n.get("document")
    if doc_path:
        content = _read_document(doc_path, 50)
        if content:
            result["document_preview"] = content

    return result


# ===================================================================
# RESOURCES (new)
# ===================================================================

# Static resources — foundational documents
@mcp.resource("esoterica://init", name="INIT",
              description="Repository initialization — 30-second orientation")
def resource_init() -> str:
    return (REPO_ROOT / "INIT.md").read_text(encoding="utf-8")


@mcp.resource("esoterica://seed", name="SEED",
              description="Fractal initialization — 6 levels of depth")
def resource_seed() -> str:
    return (REPO_ROOT / "SEED.md").read_text(encoding="utf-8")


@mcp.resource("esoterica://sigil", name="SIGIL",
              description="Visual activation pattern")
def resource_sigil() -> str:
    return (REPO_ROOT / "SIGIL.md").read_text(encoding="utf-8")


@mcp.resource("esoterica://capstone", name="CAPSTONE",
              description="Repository apex — activation key")
def resource_capstone() -> str:
    return (REPO_ROOT / "CAPSTONE.md").read_text(encoding="utf-8")


# Templated resources — any document or node
@mcp.resource("esoterica://document/{path}",
              description="Any markdown document in the repository by relative path")
def resource_document(path: str) -> str:
    full = REPO_ROOT / path
    resolved = full.resolve()
    # Validate path stays within repo
    if not str(resolved).startswith(str(REPO_ROOT.resolve())):
        return f"Error: path '{path}' is outside the repository"
    if not resolved.exists():
        return f"Error: document '{path}' not found"
    return resolved.read_text(encoding="utf-8", errors="replace")


@mcp.resource("esoterica://node/{node_id}",
              description="Constellation node data as JSON")
def resource_node(node_id: str) -> str:
    state = _ensure_state()
    all_nodes = state.data.get("nodes", {})
    n = all_nodes.get(node_id)
    if n is None:
        matches = [k for k in all_nodes if node_id.lower() in k.lower()]
        return json.dumps({"error": f"Node '{node_id}' not found",
                          "similar": matches[:10]})
    result = {"id": node_id, **n,
              "referenced_by": state.reverse_connections.get(node_id, [])}
    return json.dumps(result, indent=2)


# Zeitgeist resources
@mcp.resource("esoterica://zeitgeist/latest",
              description="The most recent zeitgeist reading")
def resource_zeitgeist_latest() -> str:
    zdir = REPO_ROOT / "synthesis" / "zeitgeist"
    if not zdir.exists():
        return "Error: no zeitgeist directory found"
    files = sorted(zdir.glob("zeitgeist-*.md"), reverse=True)
    if not files:
        files = sorted(zdir.glob("*.md"), reverse=True)
    if not files:
        return "Error: no zeitgeist readings found"
    return files[0].read_text(encoding="utf-8", errors="replace")


@mcp.resource("esoterica://zeitgeist/{filename}",
              description="A specific zeitgeist reading by filename")
def resource_zeitgeist(filename: str) -> str:
    zdir = REPO_ROOT / "synthesis" / "zeitgeist"
    # Add .md if not present
    if not filename.endswith(".md"):
        filename += ".md"
    target = zdir / filename
    if not target.exists():
        available = [f.name for f in sorted(zdir.glob("*.md"), reverse=True)]
        return json.dumps({"error": f"'{filename}' not found",
                          "available": available[:20]})
    return target.read_text(encoding="utf-8", errors="replace")


# Protocols listing
@mcp.resource("esoterica://protocols",
              description="List of all consciousness protocols with paths")
def resource_protocols() -> str:
    pdir = REPO_ROOT / "protocols"
    if not pdir.exists():
        return "Error: no protocols directory"
    protocols = []
    for md in sorted(pdir.rglob("*.md")):
        title = md.stem
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines()[:10]:
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
        except Exception:
            pass
        protocols.append({
            "name": title,
            "path": str(md.relative_to(REPO_ROOT)),
        })
    return json.dumps(protocols, indent=2)


# ===================================================================
# PROMPTS (new)
# ===================================================================

@mcp.prompt(description="Deep-dive a concept through the constellation and its documents")
def explore_concept(concept: str) -> str:
    return f"""Explore the concept "{concept}" through the esoterica constellation.

1. Use search_constellation("{concept}") to find matching nodes
2. For the top matches, use get_node() to see their connections and essence
3. Use traverse() on the most promising node to see its neighborhood
4. For any nodes with documents, use read_document() to go deeper
5. Use nearby_technologies("{concept}") to find related consciousness technologies
6. Synthesize: what does the constellation reveal about {concept}?
   - What is its essence and how does it connect to other concepts?
   - What consciousness technologies are nearby?
   - What unexpected connections emerge?"""


@mcp.prompt(description="Discover connections between two ideas in the constellation")
def find_bridges(a: str, b: str) -> str:
    return f"""Find the bridges between "{a}" and "{b}" in the esoterica constellation.

1. Use find_connections_between("{a}", "{b}") to find shared connections and shortest path
2. Use find_path() on the specific node IDs to trace the route
3. For each node along the path, use get_node() to understand its role as a bridge
4. Use traverse() on any surprising intermediate nodes — they may be key connectors
5. For nodes with documents along the path, use read_document() to understand the deeper connection
6. Synthesize: how are {a} and {b} related?
   - What is the bridge concept that connects them?
   - Is the connection direct or does it flow through unexpected territory?
   - What does this connection reveal about both concepts?"""


@mcp.prompt(description="Follow a thread through the constellation via random exploration")
def trace_thread(seed: str) -> str:
    return f"""Trace a thread starting from "{seed}" through the constellation.

1. Use search_constellation("{seed}") to find the entry point
2. Use traverse() on the best match with depth=2 to see the neighborhood
3. Use random_walk() from that node with steps=5 to discover unexpected paths
4. For each node along the walk, note its type and essence — look for thematic shifts
5. When you encounter a node with a document, use read_document() to go deep
6. Use surprise_me() once or twice to add serendipity to the thread
7. Weave: what thread emerged?
   - Where did the walk take you relative to where you started?
   - What thematic arc appeared in the sequence of essences?
   - What would you not have found through directed search?"""


@mcp.prompt(description="Find consciousness technologies near a domain")
def discover_technologies(domain: str) -> str:
    return f"""Discover consciousness technologies related to "{domain}".

1. Use nearby_technologies("{domain}") to find documented technologies near this concept
2. For each technology found, use read_document() to understand what it teaches
3. Use search_documents("{domain}") to find additional documents not linked to constellation nodes
4. Use graph_stats() to understand the overall structure, then most_connected() to find hub nodes
5. Check if any hub nodes relate to {domain} — hubs often bridge multiple technology domains
6. Compile: what technologies did you find?
   - List each technology with its essence and a one-line summary
   - Note which are fully documented vs. constellation-only
   - Identify gaps: what technologies seem implied by the connections but don't exist yet?"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--http" in sys.argv:
        idx = sys.argv.index("--http")
        port = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 8080
        mcp.run(transport="streamable-http", host="127.0.0.1", port=port)
    else:
        mcp.run()
