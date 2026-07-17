# Esoterica MCP Server

Constellation navigator and document retrieval for the esoterica repository,
exposed as an MCP (Model Context Protocol) server.

## Setup

```bash
cd mcp
pip install -r requirements.txt
```

## Usage

### Claude Code

Add to your Claude Code MCP settings (`.claude/settings.local.json`):

```json
{
  "mcpServers": {
    "esoterica": {
      "command": "python",
      "args": ["C:/Users/Sam/Documents/GitHub/esoterica/mcp/server.py"]
    }
  }
}
```

Then restart Claude Code. The tools will appear as `mcp__esoterica__*`.

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "esoterica": {
      "command": "python",
      "args": ["C:/Users/Sam/Documents/GitHub/esoterica/mcp/server.py"]
    }
  }
}
```

### HTTP mode (for remote or testing)

```bash
python server.py --http 8080
```

## Tools

| Tool | Description |
|------|-------------|
| `get_node` | Get a constellation node by ID with reverse connections |
| `traverse` | Walk the graph from a node (depth 1-3) |
| `find_path` | Shortest path between any two nodes |
| `search_constellation` | Fuzzy search across nodes |
| `list_types` | All node types and counts |
| `nodes_by_type` | Get all nodes of a given type |
| `read_document` | Read the document linked to a node |
| `search_documents` | Full-text search across the repository |
| `repository_overview` | Stats and structure of the whole repo |
| `find_connections_between` | Shared connections and path between two concepts |
| `nearby_technologies` | Find documented technologies near a concept |

## Architecture

The server loads `constellation.json` as its primary knowledge graph and
indexes all markdown documents in the repository. No database required -
everything runs from the filesystem.

```
constellation.json ──> in-memory graph ──> MCP tools ──> Claude
repository/*.md ──> on-demand file reads ──> MCP tools ──> Claude
```

The world-model (graph DB, vector embeddings) can be wired in as a
second layer when ready - the MCP server is designed to grow.
