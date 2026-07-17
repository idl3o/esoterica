"""
Graph Store: NetworkX-based knowledge graph with JSON persistence
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Set
import networkx as nx


class GraphStore:
    """
    Knowledge graph storing entities and their relationships.

    Uses NetworkX for in-memory graph operations with JSON persistence.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.graph = nx.DiGraph()
        self._entity_index: Dict[str, str] = {}  # name -> id mapping

        if self.path.exists():
            self.load()

    # ==================== ENTITY OPERATIONS ====================

    def add_entity(self, entity: Dict[str, Any]) -> str:
        """
        Add an entity to the graph.

        Args:
            entity: Dict with id, name, type, description, etc.

        Returns:
            Entity ID
        """
        entity_id = entity.get("id") or self._generate_id(entity.get("name", ""))

        # Add node with all attributes
        self.graph.add_node(
            entity_id,
            name=entity.get("name", entity_id),
            type=entity.get("type", "concept"),
            description=entity.get("description", ""),
            aliases=entity.get("aliases", []),
            tags=entity.get("tags", []),
            sources=entity.get("sources", []),
            metadata=entity.get("metadata", {})
        )

        # Update index
        name = entity.get("name", entity_id).lower()
        self._entity_index[name] = entity_id
        for alias in entity.get("aliases", []):
            self._entity_index[alias.lower()] = entity_id

        return entity_id

    def get_entity(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by name or ID"""
        # Try direct ID lookup
        if name_or_id in self.graph:
            return {"id": name_or_id, **self.graph.nodes[name_or_id]}

        # Try name index
        entity_id = self._entity_index.get(name_or_id.lower())
        if entity_id and entity_id in self.graph:
            return {"id": entity_id, **self.graph.nodes[entity_id]}

        return None

    def search_entities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search entities by name/description containing query"""
        query_lower = query.lower()
        results = []

        for node_id, data in self.graph.nodes(data=True):
            name = data.get("name", "").lower()
            desc = data.get("description", "").lower()
            tags = [t.lower() for t in data.get("tags", [])]

            if query_lower in name or query_lower in desc or query_lower in tags:
                results.append({"id": node_id, **data})
                if len(results) >= limit:
                    break

        return results

    def entity_count(self) -> int:
        """Return number of entities"""
        return self.graph.number_of_nodes()

    # ==================== RELATION OPERATIONS ====================

    def add_relation(self, relation: Dict[str, Any]) -> bool:
        """
        Add a relation between two entities.

        Args:
            relation: Dict with source, target, type, weight, etc.

        Returns:
            True if relation was added
        """
        source = relation.get("source")
        target = relation.get("target")

        if not source or not target:
            return False

        # Resolve names to IDs if needed
        source_id = self._entity_index.get(source.lower(), source)
        target_id = self._entity_index.get(target.lower(), target)

        # Add edge
        self.graph.add_edge(
            source_id,
            target_id,
            type=relation.get("type", "relates_to"),
            weight=relation.get("weight", 1.0),
            description=relation.get("description", ""),
            source_doc=relation.get("source_doc", ""),
            bidirectional=relation.get("bidirectional", False)
        )

        # Add reverse edge if bidirectional
        if relation.get("bidirectional", False):
            self.graph.add_edge(
                target_id,
                source_id,
                type=relation.get("type", "relates_to"),
                weight=relation.get("weight", 1.0),
                description=relation.get("description", ""),
                source_doc=relation.get("source_doc", ""),
                bidirectional=True
            )

        return True

    def get_relations(self, entity_name_or_id: str) -> List[Dict[str, Any]]:
        """Get all relations for an entity"""
        entity = self.get_entity(entity_name_or_id)
        if not entity:
            return []

        entity_id = entity["id"]
        relations = []

        # Outgoing relations
        for _, target, data in self.graph.out_edges(entity_id, data=True):
            relations.append({
                "source": entity_id,
                "target": target,
                "direction": "outgoing",
                **data
            })

        # Incoming relations
        for source, _, data in self.graph.in_edges(entity_id, data=True):
            relations.append({
                "source": source,
                "target": entity_id,
                "direction": "incoming",
                **data
            })

        return relations

    def relation_count(self) -> int:
        """Return number of relations"""
        return self.graph.number_of_edges()

    # ==================== GRAPH TRAVERSAL ====================

    def get_neighbors(self, entity_name_or_id: str, depth: int = 1) -> Dict[str, Any]:
        """
        Get all neighbors up to specified depth.

        Returns subgraph centered on entity.
        """
        entity = self.get_entity(entity_name_or_id)
        if not entity:
            return {"center": None, "nodes": [], "edges": []}

        entity_id = entity["id"]

        # BFS to find all nodes within depth
        visited: Set[str] = {entity_id}
        frontier = {entity_id}

        for _ in range(depth):
            next_frontier: Set[str] = set()
            for node in frontier:
                # Add successors and predecessors
                next_frontier.update(self.graph.successors(node))
                next_frontier.update(self.graph.predecessors(node))
            next_frontier -= visited
            visited.update(next_frontier)
            frontier = next_frontier

        # Build subgraph
        subgraph = self.graph.subgraph(visited)

        nodes = [{"id": n, **subgraph.nodes[n]} for n in subgraph.nodes()]
        edges = [
            {"source": u, "target": v, **d}
            for u, v, d in subgraph.edges(data=True)
        ]

        return {
            "center": entity_id,
            "nodes": nodes,
            "edges": edges
        }

    def shortest_path(self, source: str, target: str) -> List[str]:
        """Find shortest path between two entities"""
        source_entity = self.get_entity(source)
        target_entity = self.get_entity(target)

        if not source_entity or not target_entity:
            return []

        try:
            # Try undirected path
            undirected = self.graph.to_undirected()
            return nx.shortest_path(undirected, source_entity["id"], target_entity["id"])
        except nx.NetworkXNoPath:
            return []

    def get_clusters(self, algorithm: str = "louvain") -> List[Set[str]]:
        """Detect communities/clusters in the graph"""
        undirected = self.graph.to_undirected()

        if algorithm == "louvain":
            try:
                import community as community_louvain
                partition = community_louvain.best_partition(undirected)
                clusters: Dict[int, Set[str]] = {}
                for node, cluster_id in partition.items():
                    if cluster_id not in clusters:
                        clusters[cluster_id] = set()
                    clusters[cluster_id].add(node)
                return list(clusters.values())
            except ImportError:
                pass

        # Fallback to connected components
        return [set(c) for c in nx.connected_components(undirected)]

    # ==================== PERSISTENCE ====================

    def save(self):
        """Save graph to JSON file"""
        data = {
            "nodes": {
                node: dict(self.graph.nodes[node])
                for node in self.graph.nodes()
            },
            "edges": [
                {"source": u, "target": v, **d}
                for u, v, d in self.graph.edges(data=True)
            ],
            "index": self._entity_index
        }

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self):
        """Load graph from JSON file"""
        if not self.path.exists():
            return

        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.graph.clear()
        self._entity_index = data.get("index", {})

        # Add nodes
        for node_id, attrs in data.get("nodes", {}).items():
            self.graph.add_node(node_id, **attrs)

        # Add edges
        for edge in data.get("edges", []):
            source = edge.pop("source")
            target = edge.pop("target")
            self.graph.add_edge(source, target, **edge)

    # ==================== EXPORT ====================

    def to_json(self) -> str:
        """Export graph as JSON string"""
        data = {
            "nodes": [
                {"id": n, **self.graph.nodes[n]}
                for n in self.graph.nodes()
            ],
            "edges": [
                {"source": u, "target": v, **d}
                for u, v, d in self.graph.edges(data=True)
            ]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def to_graphml(self) -> str:
        """Export graph as GraphML"""
        from io import BytesIO
        buffer = BytesIO()
        nx.write_graphml(self.graph, buffer)
        return buffer.getvalue().decode('utf-8')

    # ==================== UTILITIES ====================

    def _generate_id(self, name: str) -> str:
        """Generate entity ID from name"""
        import re
        # Convert to lowercase, replace spaces/special chars with underscores
        clean = re.sub(r'[^a-z0-9]+', '_', name.lower())
        return clean.strip('_')
