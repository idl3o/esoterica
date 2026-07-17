# World Model: Local Consciousness Knowledge System
## Architecture for Integrated Knowledge Navigation

---

## Vision

A local system that:
- **Ingests** all esoterica content (markdown, JSON, transcripts, future multimedia)
- **Extracts** entities, concepts, relationships automatically
- **Stores** as queryable knowledge graph + vector embeddings
- **Visualizes** as navigable 3D world
- **Augments** local LLM interactions with relevant context
- **Evolves** as new content is added

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WORLD MODEL                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   INGEST     │───▶│   PROCESS    │───▶│    STORE     │          │
│  │              │    │              │    │              │          │
│  │ • Markdown   │    │ • Entity     │    │ • Graph DB   │          │
│  │ • JSON       │    │   extraction │    │ • Vector DB  │          │
│  │ • Transcripts│    │ • Relation   │    │ • Document   │          │
│  │ • YouTube    │    │   detection  │    │   store      │          │
│  │ • Images     │    │ • Embedding  │    │              │          │
│  │ • Audio      │    │ • Chunking   │    │              │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                 │                    │
│                                                 ▼                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                        QUERY LAYER                            │  │
│  │                                                               │  │
│  │  • Graph traversal (find connections)                        │  │
│  │  • Vector similarity (semantic search)                       │  │
│  │  • Hybrid queries (graph + vector)                           │  │
│  │  • Natural language interface                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                 │                    │
│                    ┌────────────────────────────┼────────────────┐  │
│                    ▼                            ▼                ▼  │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────┐
│  │    VISUALIZE         │  │    LLM CONTEXT       │  │    API      │
│  │                      │  │                      │  │             │
│  │ • 3D graph explorer  │  │ • RAG retrieval      │  │ • REST      │
│  │ • Document map       │  │ • Context injection  │  │ • WebSocket │
│  │ • Concept clusters   │  │ • Claude integration │  │ • CLI       │
│  │ • Timeline view      │  │ • Local LLM support  │  │             │
│  └──────────────────────┘  └──────────────────────┘  └─────────────┘
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Ingestion Layer (`/ingest`)

**Markdown Processor**
- Parse frontmatter (YAML metadata)
- Extract headers as structure
- Identify code blocks, quotes, lists
- Preserve source file reference

**JSON Processor**
- constellation.json → graph import
- synthesis-index.json → document metadata
- Egyptian/other mythology maps → entity extraction

**Transcript Processor**
- YouTube extractions → clean text + timestamps
- Speaker identification (if available)
- Topic segmentation

**Future: Multimedia**
- Images → description via vision model
- Audio → transcription + embedding
- Video → frame extraction + audio

### 2. Processing Layer (`/process`)

**Entity Extraction**
```python
# Entity types
ENTITY_TYPES = [
    "concept",           # Abstract ideas (consciousness, polarity, etc.)
    "archetype",         # Mythological figures (Mercury, Kalki, etc.)
    "tradition",         # Wisdom traditions (Hermetic, Buddhist, etc.)
    "practice",          # Techniques (meditation, reality programming)
    "person",            # Real people (Ra, Matías de Stefano, etc.)
    "place",             # Physical/mythical locations (Giza, Hyperborea)
    "text",              # Source texts (Law of One, etc.)
    "fiction",           # Fictional works (WH40K, Marvel, etc.)
    "celestial_body",    # Stars, planets, moons
    "time_period",       # Yugas, ages, eras
    "frequency",         # Densities, vibrations, harmonics
]
```

**Relation Detection**
```python
# Relation types
RELATION_TYPES = [
    "is_a",              # Taxonomy
    "part_of",           # Composition
    "relates_to",        # General connection
    "derives_from",      # Origin/source
    "transforms_into",   # Evolution/change
    "corresponds_to",    # Hermetic correspondence
    "opposes",           # Polarity
    "synthesizes",       # Integration
    "enables",           # Causation
    "mentioned_in",      # Document reference
]
```

**Embedding Generation**
- Document-level embeddings (full document → single vector)
- Chunk-level embeddings (paragraphs/sections → vectors)
- Entity embeddings (concept descriptions → vectors)
- Model: `sentence-transformers/all-MiniLM-L6-v2` (local, fast)
- Or: Ollama embeddings for fully local

**Chunking Strategy**
- Semantic chunking (by headers/sections)
- Overlap for context preservation
- Metadata preservation (source, position)

### 3. Storage Layer (`/store`)

**Graph Database**
```
Option A: NetworkX + JSON persistence (lightweight, pure Python)
Option B: SQLite + custom graph schema (more robust)
Option C: Neo4j (full-featured, but heavier)

Recommendation: Start with NetworkX + JSON, migrate if needed
```

**Vector Database**
```
Option A: ChromaDB (easy, local, persistent)
Option B: FAISS + pickle (faster, more control)
Option C: LanceDB (modern, hybrid capabilities)

Recommendation: ChromaDB for ease, or FAISS for performance
```

**Document Store**
```
Option A: SQLite (structured metadata + full text)
Option B: File system + JSON index
Option C: DuckDB (analytical queries)

Recommendation: SQLite for simplicity and full-text search
```

### 4. Query Layer (`/query`)

**Graph Queries**
```python
# Example queries
world.graph.neighbors("consciousness")           # Direct connections
world.graph.path("pyramid", "luna")              # Connection path
world.graph.cluster("archetype")                 # Related entities
world.graph.subgraph(["galactan", "borean"])     # Extract subgraph
```

**Vector Queries**
```python
# Example queries
world.vector.search("how do pyramids work")      # Semantic search
world.vector.similar("consciousness")            # Similar concepts
world.vector.cluster(n=10)                       # Auto-clustering
```

**Hybrid Queries**
```python
# Combined graph + vector
world.query("what connects pyramids to lunar dynamics")
# 1. Vector search for relevant documents
# 2. Extract entities from results
# 3. Graph traversal from those entities
# 4. Rank by combined relevance
```

**Natural Language Interface**
```python
# LLM-powered query interpretation
world.ask("How does Luna maintain Earth's stability?")
# → Interprets intent
# → Constructs appropriate query
# → Retrieves relevant context
# → Generates response with citations
```

### 5. Visualization Layer (`/visualize`)

**3D Graph Explorer**
- Extend existing Three.js implementation
- Nodes = entities (sized by connection count)
- Edges = relationships (colored by type)
- Clusters = auto-detected communities
- Navigation = click to focus, scroll to zoom

**Document Map**
- 2D projection of document embeddings (UMAP/t-SNE)
- Documents as points, colored by category
- Hover for preview, click to open
- Drag to explore neighborhoods

**Concept Clusters**
- Hierarchical view of entity taxonomy
- Expandable/collapsible tree
- Search to highlight paths

**Timeline View**
- Documents/entities arranged by creation/mention date
- Precessional ages, yugas overlaid
- Zoom from cosmic to session scale

### 6. LLM Context Layer (`/context`)

**RAG Retrieval**
```python
def get_context(query: str, k: int = 5) -> str:
    """Retrieve relevant context for LLM prompt"""
    # Vector search for relevant chunks
    chunks = world.vector.search(query, k=k)

    # Expand with graph neighbors
    entities = extract_entities(chunks)
    related = world.graph.neighbors(entities, depth=1)

    # Format for injection
    return format_context(chunks, related)
```

**Claude Integration**
- MCP server exposing world model queries
- Auto-context injection for esoterica questions
- Citation tracking back to source documents

**Local LLM Support**
- Ollama integration for offline use
- Context window optimization
- Prompt templates for different models

### 7. API Layer (`/api`)

**REST Endpoints**
```
GET  /entities                    # List all entities
GET  /entities/{id}               # Get entity details
GET  /entities/{id}/connections   # Get entity connections
GET  /documents                   # List all documents
GET  /documents/{id}              # Get document content
POST /search                      # Hybrid search
POST /query                       # Natural language query
GET  /graph                       # Export full graph
GET  /stats                       # System statistics
```

**WebSocket**
- Real-time graph updates
- Live query streaming
- Visualization sync

**CLI**
```bash
world-model ingest              # Re-ingest all content
world-model search "query"      # Quick search
world-model graph show          # Open visualization
world-model context "query"     # Get LLM context
world-model stats               # Show statistics
```

---

## Data Schema

### Entity
```json
{
  "id": "uuid",
  "name": "Galactan Mechanism",
  "type": "concept",
  "description": "Earth's connection to galactic frequencies via pyramid network",
  "aliases": ["galactic connection", "pyramid antenna"],
  "embedding": [0.1, 0.2, ...],
  "sources": ["synthesis/cosmological/galactan-mechanism-pyramid-maintenance.md"],
  "created": "2026-01-13",
  "metadata": {
    "category": "consciousness-technology",
    "tags": ["pyramid", "galactic", "frequency"]
  }
}
```

### Relation
```json
{
  "id": "uuid",
  "source": "entity_id",
  "target": "entity_id",
  "type": "enables",
  "weight": 0.8,
  "description": "Luna enables borean mechanism",
  "sources": ["synthesis/cosmological/ode-to-the-sun.md"],
  "bidirectional": false
}
```

### Document
```json
{
  "id": "uuid",
  "path": "synthesis/cosmological/galactan-mechanism.md",
  "title": "The Galactan Mechanism",
  "category": "cosmological",
  "tags": ["pyramid", "galactic", "luna"],
  "content": "full text...",
  "chunks": [
    {"id": "chunk_1", "text": "...", "embedding": [...], "position": 0}
  ],
  "entities_mentioned": ["entity_id_1", "entity_id_2"],
  "created": "2026-01-13",
  "modified": "2026-01-13"
}
```

---

## File Structure

```
world-model/
├── ARCHITECTURE.md          # This file
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
│
├── src/
│   ├── __init__.py
│   ├── world.py             # Main WorldModel class
│   │
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── markdown.py      # Markdown processor
│   │   ├── json.py          # JSON processor
│   │   ├── transcript.py    # Transcript processor
│   │   └── multimedia.py    # Future: images, audio
│   │
│   ├── process/
│   │   ├── __init__.py
│   │   ├── entities.py      # Entity extraction
│   │   ├── relations.py     # Relation detection
│   │   ├── embeddings.py    # Embedding generation
│   │   └── chunking.py      # Document chunking
│   │
│   ├── store/
│   │   ├── __init__.py
│   │   ├── graph.py         # Graph database
│   │   ├── vectors.py       # Vector database
│   │   └── documents.py     # Document store
│   │
│   ├── query/
│   │   ├── __init__.py
│   │   ├── graph_query.py   # Graph queries
│   │   ├── vector_query.py  # Vector queries
│   │   ├── hybrid.py        # Combined queries
│   │   └── natural.py       # NL interface
│   │
│   ├── context/
│   │   ├── __init__.py
│   │   ├── rag.py           # RAG retrieval
│   │   ├── claude.py        # Claude integration
│   │   └── local_llm.py     # Ollama integration
│   │
│   └── api/
│       ├── __init__.py
│       ├── rest.py          # REST API
│       ├── websocket.py     # WebSocket server
│       └── cli.py           # CLI interface
│
├── visualize/
│   ├── index.html           # Main visualization
│   ├── graph-3d.js          # 3D graph explorer
│   ├── document-map.js      # 2D document projection
│   └── timeline.js          # Timeline view
│
├── data/
│   ├── graph.json           # Persisted graph
│   ├── vectors/             # ChromaDB/FAISS storage
│   ├── documents.db         # SQLite document store
│   └── cache/               # Embedding cache
│
├── tests/
│   └── ...
│
└── scripts/
    ├── ingest_all.py        # Full ingestion script
    ├── build_graph.py       # Graph construction
    └── serve.py             # Start all services
```

---

## Implementation Phases

### Phase 1: Foundation (MVP)
- [ ] Basic markdown ingestion
- [ ] Simple entity extraction (regex + keywords)
- [ ] NetworkX graph with JSON persistence
- [ ] ChromaDB vector store
- [ ] CLI search interface
- [ ] Basic 3D visualization (extend existing)

### Phase 2: Intelligence
- [ ] LLM-powered entity extraction
- [ ] Relation detection
- [ ] Hybrid query system
- [ ] Natural language interface
- [ ] RAG context generation

### Phase 3: Integration
- [ ] Claude MCP server
- [ ] REST API
- [ ] WebSocket live updates
- [ ] Document map visualization
- [ ] Local LLM support (Ollama)

### Phase 4: Evolution
- [ ] Multimedia ingestion
- [ ] Auto-updating from file changes
- [ ] Community/sharing features
- [ ] Timeline visualization
- [ ] Mobile interface

---

## Dependencies

```txt
# Core
python >= 3.10
networkx >= 3.0
chromadb >= 0.4.0
sentence-transformers >= 2.2.0
sqlite3 (stdlib)

# Processing
pyyaml >= 6.0
markdown >= 3.4
beautifulsoup4 >= 4.12

# API
fastapi >= 0.100.0
uvicorn >= 0.23.0
websockets >= 11.0

# CLI
click >= 8.1
rich >= 13.0

# Visualization
# (JavaScript - Three.js, D3.js already in repo)

# Optional
ollama >= 0.1.0           # Local LLM
anthropic >= 0.18.0       # Claude API
openai >= 1.0.0           # Embeddings alternative
```

---

## Quick Start (After Implementation)

```bash
# Install
cd world-model
pip install -e .

# Ingest all esoterica content
world-model ingest --all

# Search
world-model search "how do pyramids connect to galactic frequencies"

# Start visualization server
world-model serve

# Get LLM context
world-model context "explain the borean mechanism" | pbcopy
```

---

## Integration with Existing Esoterica

**constellation.json** → Direct import as graph foundation
**synthesis-index.json** → Document metadata bootstrap
**Existing 3D explorer** → Extend rather than replace
**YouTube extractions** → Already in compatible format
**CLAUDE.md** → Entity extraction for core concepts

---

## Open Questions

1. **Entity extraction approach**: Rule-based vs LLM-powered vs hybrid?
2. **Embedding model**: Local (sentence-transformers) vs API (OpenAI)?
3. **Graph persistence**: JSON files vs SQLite vs Neo4j?
4. **Visualization framework**: Extend Three.js or use dedicated (vis.js, cytoscape)?
5. **LLM integration**: Claude API, local Ollama, or both?

---

*Architecture drafted: January 2026*
*Ready for implementation*
