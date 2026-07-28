# Constellation

The living graph. `constellation.json` holds ~1,050 nodes — consciousness
technologies, concepts, documents, and the connections between them — and is the
single source the site reads to render the explorer and the node pages.

## The canonical writer

**Write to the graph through the MCP `add_node` / `add_connection` / `update_node`
tools** (`apparatus/mcp/server.py`), not by hand and not through the legacy Python
scripts. The MCP path is what the `.claude/workflows/*` automations use, it is
single-writer-safe, and it keeps one consistent serialization — which is why the
graph no longer needs the ad-hoc brace-repair hacks earlier batch writers left
downstream. One writer, one format.

`serve_constellation.py` is the local viewer/server for the JSON and is fine to run.

## Legacy scripts (archival)

These are one-shot integration tools from earlier graph-building batches. They are
kept for reference and reproducibility, **not** maintained, and should not be the
path you reach for to add nodes — prefer the MCP tools above:

- `add_2026_01_25_nodes.py`, `constellation_connect_new_nodes.py` — dated batch adds
- `constellation_batch_integrate.py`, `constellation_integrate.py` — bulk integration
- `constellation_polish.py`, `constellation_weaver.py` — one-shot passes
- `world_tree_generator.py` — world-tree derivation

If you revive one, make it write through the MCP layer rather than editing
`constellation.json` directly, so the single-writer invariant holds.
