"""Tests for the esoterica MCP server.  Run:  python -m pytest apparatus/mcp

FastMCP derives each tool's output schema from its return annotation and
validates every result against it before the client sees anything, so a
return annotation narrower than the payload makes the tool fail on every
call. These tests drive the tools through FastMCP's own call path so that
validation is exercised, not bypassed.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import server  # noqa: E402


@pytest.fixture(scope="module")
def state():
    """Load the live constellation once, without the TF-IDF corpus index."""
    mtime = server.CONSTELLATION_PATH.stat().st_mtime
    server._state = server._build_state(mtime, build_tfidf=False)
    return server._state


def call(name: str, **args):
    return asyncio.run(server.mcp.call_tool(name, args))


def test_nodes_by_type_survives_output_validation(state):
    """Regression: `connections_count` is an int and `has_document` a bool;
    the annotation `list[dict[str, str]]` rejected every real row."""
    some_type = next(iter(state.type_index))
    content, structured = call("nodes_by_type", node_type=some_type)
    rows = structured["result"]
    assert rows, "a populated type should return rows"
    first = rows[0]
    assert isinstance(first["connections_count"], int)
    assert isinstance(first["has_document"], bool)
    assert len(rows) == len(state.type_index[some_type])


def test_nodes_by_type_unknown_type_reports_available(state):
    _, structured = call("nodes_by_type", node_type="no_such_type")
    rows = structured["result"]
    assert len(rows) == 1 and "error" in rows[0]
    assert "available_types" in rows[0]


@pytest.mark.parametrize("name,args", [
    ("list_types", {}),
    ("graph_stats", {}),
    ("orphan_nodes", {}),
    ("most_connected", {"n": 3}),
    ("search_constellation", {"query": "transformation", "max_results": 3}),
    ("get_node", {"node_id": "transformation"}),
    ("traverse", {"start": "transformation", "depth": 1}),
    ("find_path", {"source": "transformation", "target": "evolution"}),
])
def test_read_only_tools_validate(state, name, args):
    """Every read-only tool must round-trip through FastMCP output validation."""
    _, structured = call(name, **args)
    assert structured is not None
