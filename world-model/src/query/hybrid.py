"""
Hybrid Query: Combined graph + vector search
"""

from typing import List, Dict, Any, Optional


class HybridQuery:
    """
    Hybrid query engine combining:
    - Vector similarity search (semantic)
    - Graph traversal (relational)
    - Full-text search (keyword)

    Results are merged and ranked by combined relevance.
    """

    def __init__(self, graph, vectors, documents):
        self.graph = graph
        self.vectors = vectors
        self.documents = documents
        self._embedder = None

    def _get_embedder(self):
        """Lazy load embedder"""
        if self._embedder is None:
            try:
                from ..process.embeddings import EmbeddingGenerator
            except ImportError:
                from process.embeddings import EmbeddingGenerator
            self._embedder = EmbeddingGenerator()
        return self._embedder

    def search(self, query: str, k: int = 10,
               weights: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """
        Hybrid search combining multiple strategies.

        Args:
            query: Natural language query
            k: Number of results
            weights: Optional weights for each strategy
                     {"vector": 0.5, "graph": 0.3, "text": 0.2}

        Returns:
            Ranked list of results with combined scores
        """
        weights = weights or {"vector": 0.5, "graph": 0.3, "text": 0.2}

        results = {}

        # Vector similarity search
        if weights.get("vector", 0) > 0:
            vector_results = self._vector_search(query, k * 2)
            for r in vector_results:
                rid = r.get("id", "")
                if rid not in results:
                    results[rid] = {"id": rid, "content": r.get("content", ""), "scores": {}}
                results[rid]["scores"]["vector"] = r.get("score", 0)
                results[rid]["source"] = r.get("metadata", {}).get("doc_id", rid)

        # Graph-based search
        if weights.get("graph", 0) > 0:
            graph_results = self._graph_search(query, k * 2)
            for r in graph_results:
                rid = r.get("id", "")
                if rid not in results:
                    results[rid] = {"id": rid, "content": r.get("content", ""), "scores": {}}
                results[rid]["scores"]["graph"] = r.get("score", 0)

        # Full-text search
        if weights.get("text", 0) > 0:
            text_results = self._text_search(query, k * 2)
            for r in text_results:
                rid = r.get("id", "")
                if rid not in results:
                    results[rid] = {"id": rid, "content": r.get("content", ""), "scores": {}}
                results[rid]["scores"]["text"] = r.get("score", 0)
                results[rid]["source"] = r.get("path", rid)

        # Calculate combined scores
        for rid, data in results.items():
            combined = 0
            for strategy, weight in weights.items():
                combined += data["scores"].get(strategy, 0) * weight
            data["combined_score"] = combined

        # Sort by combined score
        ranked = sorted(results.values(), key=lambda x: x["combined_score"], reverse=True)

        return ranked[:k]

    def _vector_search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Semantic similarity search"""
        embedder = self._get_embedder()
        query_embedding = embedder.embed_text(query)
        return self.vectors.search(query_embedding, k=k)

    def _graph_search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Graph-based search - find entities matching query terms"""
        results = []

        # Search for matching entities
        entities = self.graph.search_entities(query, limit=k)

        for entity in entities:
            # Get neighbors for context
            neighbors = self.graph.get_neighbors(entity["id"], depth=1)

            results.append({
                "id": entity["id"],
                "content": entity.get("description", entity.get("name", "")),
                "score": 0.8,  # Base score for direct match
                "type": "entity",
                "neighbors": len(neighbors.get("nodes", []))
            })

        return results

    def _text_search(self, query: str, k: int) -> List[Dict[str, Any]]:
        """Full-text search in documents"""
        try:
            results = self.documents.search(query, limit=k)
            for r in results:
                # Normalize score (FTS5 BM25 scores are negative, lower is better)
                r["score"] = 1.0 / (1.0 + abs(r.get("score", 0)))
            return results
        except Exception:
            return []

    def find_connections(self, entity1: str, entity2: str) -> Dict[str, Any]:
        """
        Find how two entities are connected.

        Returns path and intermediate nodes.
        """
        path = self.graph.shortest_path(entity1, entity2)

        if not path:
            return {"connected": False, "path": []}

        # Get details for each node in path
        nodes = []
        for node_id in path:
            entity = self.graph.get_entity(node_id)
            if entity:
                nodes.append(entity)

        return {
            "connected": True,
            "path": path,
            "nodes": nodes,
            "distance": len(path) - 1
        }

    def explore(self, start: str, depth: int = 2) -> Dict[str, Any]:
        """
        Explore graph from a starting entity.

        Returns subgraph for visualization.
        """
        return self.graph.get_neighbors(start, depth=depth)
