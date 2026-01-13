# World Model

Local consciousness knowledge system for the Esoterica repository.

## Features

- **Knowledge Graph**: Entities and relationships from all synthesis documents
- **Vector Embeddings**: Semantic search across 200+ documents
- **Hybrid Query**: Combined graph traversal + vector similarity
- **LLM Context**: Auto-generate relevant context for AI conversations
- **CLI Interface**: Quick access from terminal

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .

# Ingest all content
python run.py ingest

# Search
python run.py search "how do pyramids work"

# Explore entity connections
python run.py explore "consciousness"

# Find path between concepts
python run.py path "luna" "pyramid"

# Get LLM context
python run.py context "explain the galactan mechanism"

# View stats
python run.py stats
```

## Architecture

```
world-model/
├── src/
│   ├── world.py          # Main WorldModel class
│   ├── ingest/           # Document parsing
│   ├── process/          # Entity extraction, embeddings
│   ├── store/            # Graph, vector, document storage
│   ├── query/            # Hybrid search engine
│   └── cli.py            # Command-line interface
├── data/                 # Persistent storage (auto-created)
└── visualize/            # 3D visualization (future)
```

## Data Flow

```
Markdown Files → Parse → Extract Entities → Generate Embeddings → Store
                                                                    ↓
Query ← Hybrid Search ← Graph + Vectors + Full-Text ← Retrieve ← Store
```

## API (Planned)

```python
from world_model import WorldModel

world = WorldModel()
world.ingest_all()

# Search
results = world.search("consciousness evolution")

# Explore graph
connections = world.get_connections("pyramid", depth=2)

# Get LLM context
context = world.get_context("what is the borean mechanism?")
```

## Integration with Claude

The world model can provide context for Claude conversations:

```python
context = world.get_context(user_question)
prompt = f"""
Based on the following esoterica knowledge:

{context}

Please answer: {user_question}
"""
```

Future: MCP server integration for automatic context injection.

---

*Part of the Esoterica consciousness technology distribution network*
