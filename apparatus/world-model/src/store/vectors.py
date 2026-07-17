"""
Vector Store: ChromaDB-based vector database for semantic search
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import json


class VectorStore:
    """
    Vector database for semantic similarity search.

    Uses ChromaDB for persistent vector storage with metadata.
    Falls back to simple in-memory storage if ChromaDB unavailable.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self._use_chroma = False
        self._client = None
        self._collection = None

        # Fallback storage
        self._vectors: Dict[str, Dict[str, Any]] = {}
        self._chunks: Dict[str, Dict[str, Any]] = {}

        self._init_storage()

    def _init_storage(self):
        """Initialize ChromaDB or fallback storage"""
        try:
            import chromadb
            from chromadb.config import Settings

            self.path.mkdir(parents=True, exist_ok=True)

            self._client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=str(self.path),
                anonymized_telemetry=False
            ))

            self._collection = self._client.get_or_create_collection(
                name="esoterica",
                metadata={"hnsw:space": "cosine"}
            )

            self._use_chroma = True
            print("Using ChromaDB for vector storage")

        except ImportError:
            print("ChromaDB not available, using fallback storage")
            self._load_fallback()

        except Exception as e:
            print(f"ChromaDB init failed ({e}), using fallback storage")
            self._load_fallback()

    # ==================== ENTITY VECTORS ====================

    def add_entity(self, entity_id: str, entity: Dict[str, Any], embedding: List[float]):
        """Add entity embedding to vector store"""
        if self._use_chroma:
            self._collection.upsert(
                ids=[f"entity::{entity_id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "entity",
                    "entity_id": entity_id,
                    "name": entity.get("name", ""),
                    "entity_type": entity.get("type", "concept")
                }],
                documents=[entity.get("description", "")]
            )
        else:
            self._vectors[f"entity::{entity_id}"] = {
                "embedding": embedding,
                "metadata": {
                    "type": "entity",
                    "entity_id": entity_id,
                    "name": entity.get("name", ""),
                    "entity_type": entity.get("type", "concept")
                },
                "document": entity.get("description", "")
            }

    # ==================== CHUNK VECTORS ====================

    def add_chunk(self, chunk_id: str, chunk: Dict[str, Any], embedding: List[float], doc_id: str):
        """Add document chunk embedding to vector store"""
        if self._use_chroma:
            self._collection.upsert(
                ids=[f"chunk::{chunk_id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "chunk",
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "position": chunk.get("position", 0)
                }],
                documents=[chunk.get("text", "")]
            )
        else:
            self._chunks[f"chunk::{chunk_id}"] = {
                "embedding": embedding,
                "metadata": {
                    "type": "chunk",
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "position": chunk.get("position", 0)
                },
                "document": chunk.get("text", "")
            }

    def chunk_count(self) -> int:
        """Return number of chunks stored"""
        if self._use_chroma:
            results = self._collection.get(where={"type": "chunk"})
            return len(results["ids"]) if results else 0
        return len(self._chunks)

    # ==================== SEARCH ====================

    def search(self, embedding: List[float], k: int = 10,
               filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.

        Args:
            embedding: Query embedding
            k: Number of results
            filter_type: Optional filter ("entity" or "chunk")

        Returns:
            List of results with scores
        """
        if self._use_chroma:
            where = {"type": filter_type} if filter_type else None

            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=k,
                where=where,
                include=["documents", "metadatas", "distances"]
            )

            if not results or not results["ids"]:
                return []

            return [
                {
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                    "score": 1 - results["distances"][0][i] if results["distances"] else 1
                }
                for i in range(len(results["ids"][0]))
            ]
        else:
            return self._fallback_search(embedding, k, filter_type)

    def search_entities(self, embedding: List[float], k: int = 10) -> List[Dict[str, Any]]:
        """Search only entity vectors"""
        return self.search(embedding, k, filter_type="entity")

    def search_chunks(self, embedding: List[float], k: int = 10) -> List[Dict[str, Any]]:
        """Search only chunk vectors"""
        return self.search(embedding, k, filter_type="chunk")

    # ==================== FALLBACK OPERATIONS ====================

    def _fallback_search(self, embedding: List[float], k: int,
                         filter_type: Optional[str]) -> List[Dict[str, Any]]:
        """Simple cosine similarity search for fallback mode"""
        import math

        def cosine_similarity(a: List[float], b: List[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            if norm_a == 0 or norm_b == 0:
                return 0
            return dot / (norm_a * norm_b)

        # Combine vectors and chunks
        all_items = {}
        if filter_type != "chunk":
            all_items.update(self._vectors)
        if filter_type != "entity":
            all_items.update(self._chunks)

        # Calculate similarities
        scored = []
        for item_id, item in all_items.items():
            score = cosine_similarity(embedding, item["embedding"])
            scored.append({
                "id": item_id,
                "content": item.get("document", ""),
                "metadata": item.get("metadata", {}),
                "score": score,
                "distance": 1 - score
            })

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:k]

    def _load_fallback(self):
        """Load fallback storage from disk"""
        vectors_file = self.path / "vectors_fallback.json"
        chunks_file = self.path / "chunks_fallback.json"

        if vectors_file.exists():
            with open(vectors_file, 'r') as f:
                self._vectors = json.load(f)

        if chunks_file.exists():
            with open(chunks_file, 'r') as f:
                self._chunks = json.load(f)

    # ==================== PERSISTENCE ====================

    def save(self):
        """Persist vector store"""
        if self._use_chroma:
            self._client.persist()
        else:
            self.path.mkdir(parents=True, exist_ok=True)

            with open(self.path / "vectors_fallback.json", 'w') as f:
                json.dump(self._vectors, f)

            with open(self.path / "chunks_fallback.json", 'w') as f:
                json.dump(self._chunks, f)

    def load(self):
        """Load vector store (ChromaDB auto-loads, fallback needs explicit load)"""
        if not self._use_chroma:
            self._load_fallback()
