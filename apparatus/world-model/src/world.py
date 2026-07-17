"""
WorldModel: Main orchestration class for the knowledge system
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# Local imports - use try/except for both relative and absolute
try:
    from .store.graph import GraphStore
    from .store.vectors import VectorStore
    from .store.documents import DocumentStore
    from .ingest.markdown import MarkdownIngester
    from .process.entities import EntityExtractor
    from .process.embeddings import EmbeddingGenerator
    from .query.hybrid import HybridQuery
except ImportError:
    from store.graph import GraphStore
    from store.vectors import VectorStore
    from store.documents import DocumentStore
    from ingest.markdown import MarkdownIngester
    from process.entities import EntityExtractor
    from process.embeddings import EmbeddingGenerator
    from query.hybrid import HybridQuery


@dataclass
class WorldModelConfig:
    """Configuration for WorldModel"""
    base_path: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_path: Path = field(default_factory=lambda: Path(__file__).parent.parent / "data")
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50


class WorldModel:
    """
    Main interface to the consciousness knowledge system.

    Integrates:
    - Graph database (entities + relations)
    - Vector database (semantic embeddings)
    - Document store (full text + metadata)
    - Query engine (hybrid graph + vector)
    """

    def __init__(self, config: Optional[WorldModelConfig] = None):
        self.config = config or WorldModelConfig()
        self._ensure_data_dirs()

        # Initialize stores
        self.graph = GraphStore(self.config.data_path / "graph.json")
        self.vectors = VectorStore(self.config.data_path / "vectors")
        self.documents = DocumentStore(self.config.data_path / "documents.db")

        # Initialize processors
        self.ingester = MarkdownIngester()
        self.entity_extractor = EntityExtractor()
        self.embedder = EmbeddingGenerator(self.config.embedding_model)

        # Initialize query engine
        self.query_engine = HybridQuery(self.graph, self.vectors, self.documents)

    def _ensure_data_dirs(self):
        """Create data directories if they don't exist"""
        self.config.data_path.mkdir(parents=True, exist_ok=True)
        (self.config.data_path / "vectors").mkdir(exist_ok=True)
        (self.config.data_path / "cache").mkdir(exist_ok=True)

    # ==================== INGESTION ====================

    def ingest_all(self, force: bool = False) -> Dict[str, int]:
        """
        Ingest all content from the esoterica repository.

        Args:
            force: If True, re-ingest even if already processed

        Returns:
            Statistics about ingested content
        """
        stats = {
            "documents": 0,
            "entities": 0,
            "relations": 0,
            "chunks": 0
        }

        # Define content directories
        content_dirs = [
            "synthesis",
            "distillations",
            "protocols",
            "extractions",
            "translated",
            "seeds",
            "traditions",
            "fiction-bridges",
            "journey",
            "correspondences",
            "harvest",
            "garden"
        ]

        for dir_name in content_dirs:
            dir_path = self.config.base_path / dir_name
            if dir_path.exists():
                dir_stats = self.ingest_directory(dir_path, force=force)
                for key in stats:
                    stats[key] += dir_stats.get(key, 0)

        # Import constellation.json as graph foundation
        constellation_path = self.config.base_path / "constellation" / "constellation.json"
        if constellation_path.exists():
            self._import_constellation(constellation_path)

        # Save all stores
        self.save()

        return stats

    def ingest_directory(self, path: Path, force: bool = False) -> Dict[str, int]:
        """Ingest all markdown files in a directory"""
        stats = {"documents": 0, "entities": 0, "relations": 0, "chunks": 0}

        for md_file in path.rglob("*.md"):
            try:
                doc_stats = self.ingest_document(md_file, force=force)
                for key in stats:
                    stats[key] += doc_stats.get(key, 0)
            except Exception as e:
                print(f"Error ingesting {md_file}: {e}")

        return stats

    def ingest_document(self, path: Path, force: bool = False) -> Dict[str, int]:
        """
        Ingest a single document.

        1. Parse markdown
        2. Extract entities
        3. Generate embeddings
        4. Store in all databases
        """
        stats = {"documents": 0, "entities": 0, "relations": 0, "chunks": 0}

        # Check if already processed
        doc_id = str(path.relative_to(self.config.base_path))
        if not force and self.documents.exists(doc_id):
            return stats

        # Parse document
        doc = self.ingester.parse(path)
        if not doc:
            return stats

        # Extract entities
        entities, relations = self.entity_extractor.extract(doc)

        # Generate embeddings
        doc_embedding = self.embedder.embed_document(doc)
        chunk_embeddings = self.embedder.embed_chunks(doc.chunks)

        # Convert ParsedDocument to dict for storage
        doc_dict = {
            "title": doc.title,
            "path": doc.path,
            "category": doc.category,
            "content": doc.content,
            "tags": doc.tags,
            "metadata": doc.metadata,
            "created": doc.frontmatter.get("created", "") if doc.frontmatter else ""
        }

        # Store document
        self.documents.store(doc_id, doc_dict, doc_embedding)
        stats["documents"] = 1
        stats["chunks"] = len(doc.chunks)

        # Store entities and relations in graph
        for entity in entities:
            entity_dict = entity.to_dict() if hasattr(entity, 'to_dict') else entity
            entity_id = entity_dict.get('id', entity_dict.get('name', ''))
            self.graph.add_entity(entity_dict)
            desc = entity.description if hasattr(entity, 'description') else entity_dict.get('description', '')
            embedding = self.embedder.embed_text(desc) if desc else self.embedder.embed_text(entity_id)
            self.vectors.add_entity(entity_id, entity_dict, embedding)
            stats["entities"] += 1

        for relation in relations:
            rel_dict = relation.to_dict() if hasattr(relation, 'to_dict') else relation
            self.graph.add_relation(rel_dict)
            stats["relations"] += 1

        # Store chunks in vector db
        for i, (chunk, embedding) in enumerate(zip(doc.chunks, chunk_embeddings)):
            chunk_dict = {"text": chunk.text, "position": chunk.position}
            self.vectors.add_chunk(f"{doc_id}::{i}", chunk_dict, embedding, doc_id)

        return stats

    def _import_constellation(self, path: Path):
        """Import constellation.json as graph foundation"""
        with open(path, 'r', encoding='utf-8') as f:
            constellation = json.load(f)

        # Import nodes as entities
        if "nodes" in constellation:
            for node_id, node_data in constellation["nodes"].items():
                entity = {
                    "id": node_id,
                    "name": node_data.get("name", node_id),
                    "type": node_data.get("type", "concept"),
                    "description": node_data.get("description", ""),
                    "tags": node_data.get("tags", []),
                    "source": "constellation.json"
                }
                self.graph.add_entity(entity)

        # Import connections as relations
        if "connections" in constellation:
            for conn in constellation["connections"]:
                relation = {
                    "source": conn.get("from"),
                    "target": conn.get("to"),
                    "type": conn.get("type", "relates_to"),
                    "weight": conn.get("weight", 1.0),
                    "source_doc": "constellation.json"
                }
                self.graph.add_relation(relation)

    # ==================== QUERYING ====================

    def search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """
        Hybrid search combining vector similarity and graph relevance.

        Args:
            query: Natural language query
            k: Number of results to return

        Returns:
            List of relevant documents/chunks with scores
        """
        return self.query_engine.search(query, k=k)

    def find_entity(self, name: str) -> Optional[Dict[str, Any]]:
        """Find an entity by name"""
        return self.graph.get_entity(name)

    def get_connections(self, entity_name: str, depth: int = 1) -> Dict[str, Any]:
        """Get all connections for an entity up to specified depth"""
        return self.graph.get_neighbors(entity_name, depth=depth)

    def find_path(self, source: str, target: str) -> List[str]:
        """Find shortest path between two entities"""
        return self.graph.shortest_path(source, target)

    def similar(self, text: str, k: int = 10) -> List[Dict[str, Any]]:
        """Find similar documents/chunks by semantic similarity"""
        embedding = self.embedder.embed_text(text)
        return self.vectors.search(embedding, k=k)

    # ==================== CONTEXT GENERATION ====================

    def get_context(self, query: str, k: int = 5) -> str:
        """
        Generate context string for LLM augmentation.

        Args:
            query: The question/topic needing context
            k: Number of context chunks to include

        Returns:
            Formatted context string for prompt injection
        """
        results = self.search(query, k=k)

        context_parts = []
        for result in results:
            source = result.get("source", "unknown")
            content = result.get("content", "")
            context_parts.append(f"[Source: {source}]\n{content}")

        return "\n\n---\n\n".join(context_parts)

    # ==================== PERSISTENCE ====================

    def save(self):
        """Save all stores to disk"""
        self.graph.save()
        self.vectors.save()
        self.documents.save()

    def load(self):
        """Load all stores from disk"""
        self.graph.load()
        self.vectors.load()
        self.documents.load()

    # ==================== STATISTICS ====================

    def stats(self) -> Dict[str, Any]:
        """Get statistics about the world model"""
        return {
            "entities": self.graph.entity_count(),
            "relations": self.graph.relation_count(),
            "documents": self.documents.count(),
            "chunks": self.vectors.chunk_count(),
            "last_updated": datetime.now().isoformat()
        }

    # ==================== EXPORT ====================

    def export_graph(self, format: str = "json") -> str:
        """Export the knowledge graph"""
        if format == "json":
            return self.graph.to_json()
        elif format == "graphml":
            return self.graph.to_graphml()
        else:
            raise ValueError(f"Unknown format: {format}")
