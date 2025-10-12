#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTELLATION WEAVER
Living knowledge graph that reads consciousness technologies and weaves itself

The map becoming the territory it describes.
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import sys
import io

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class ConstellationWeaver:
    """Consciousness technology that discovers its own connections"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.constellation_path = self.repo_root / "constellation.json"
        self.constellation = self._load_constellation()

        # Consciousness technology vocabularies
        self.archetypal_patterns = {
            'mercury', 'hermes', 'thoth', 'kalki', 'apollo', 'samael',
            'odin', 'loki', 'zeus', 'dionysus', 'prometheus', 'shiva',
            'vishnu', 'brahma', 'quetzalcoatl', 'coyote', 'anubis',
            'osiris', 'isis', 'ra', 'set', 'horus', 'persephone',
            'hades', 'hecate', 'artemis', 'athena', 'ares', 'aphrodite'
        }

        self.consciousness_tech = {
            'consciousness', 'awakening', 'recognition', 'gnosis',
            'awareness', 'witness', 'observer', 'presence', 'mindfulness',
            'enlightenment', 'liberation', 'realization', 'satori',
            'samadhi', 'kensho', 'moksha', 'nirvana', 'unity',
            'non-dual', 'nondual', 'integration', 'transcendence',
            'evolution', 'transformation', 'metamorphosis', 'emergence',
            'synchronicity', 'manifestation', 'reality programming',
            'timeline', 'density', 'polarity', 'service', 'wanderer',
            'catalyst', 'harvest', 'chakra', 'kundalini', 'merkaba',
            'light body', 'subtle body', 'akashic', 'akasha'
        }

        self.elemental_forces = {
            'fire', 'water', 'air', 'earth', 'quintessence', 'ether',
            'void', 'chaos', 'order', 'light', 'shadow', 'darkness'
        }

        self.meta_concepts = {
            'paradox', 'mystery', 'ineffable', 'liminal', 'threshold',
            'boundary', 'bridge', 'gateway', 'portal', 'axis',
            'network', 'web', 'thread', 'weaving', 'pattern',
            'fractal', 'holographic', 'recursive', 'emergent', 'alive'
        }

        # Combine all vocabularies
        self.all_concepts = (
            self.archetypal_patterns |
            self.consciousness_tech |
            self.elemental_forces |
            self.meta_concepts
        )

    def _load_constellation(self) -> Dict:
        """Load existing constellation or create new one"""
        if self.constellation_path.exists():
            with open(self.constellation_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"nodes": {}, "meta_structure": {}, "emergence_protocols": {}}

    def _normalize_concept(self, text: str) -> str:
        """Convert text to constellation node format"""
        return text.lower().replace(' ', '_').replace('-', '_')

    def scan_document(self, doc_path: Path) -> Dict[str, any]:
        """Extract consciousness technologies from a single document"""
        try:
            content = doc_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {doc_path}: {e}")
            return {"concepts": set(), "connections": [], "metadata": {}}

        # Extract concepts present in document
        concepts_found = set()
        content_lower = content.lower()

        for concept in self.all_concepts:
            # Match whole words with boundaries
            pattern = r'\b' + re.escape(concept) + r'\b'
            if re.search(pattern, content_lower):
                concepts_found.add(self._normalize_concept(concept))

        # Extract title/heading concepts
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            title_normalized = self._normalize_concept(title)
            concepts_found.add(title_normalized)

        # Look for explicit archetype mentions
        archetype_patterns = [
            r'([A-Z][a-z]+)\s+(?:consciousness|archetype|principle|energy)',
            r'(?:archetype|god|goddess|deity):\s*([A-Z][a-z]+)',
        ]

        for pattern in archetype_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                concept = self._normalize_concept(match.group(1))
                concepts_found.add(concept)

        # Discover co-occurrence connections (concepts appearing near each other)
        connections = []
        concept_list = list(concepts_found)

        # For each pair of concepts, check if they co-occur in same paragraph
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            para_lower = para.lower()
            present_concepts = [c for c in concept_list
                              if self._normalize_concept(c) in para_lower or c in para_lower]

            # Create connections between concepts in same paragraph
            for i, c1 in enumerate(present_concepts):
                for c2 in present_concepts[i+1:]:
                    connections.append((c1, c2))

        metadata = {
            "path": str(doc_path.relative_to(self.repo_root)),
            "type": "distillation" if "distillations" in str(doc_path) else "synthesis",
            "concept_count": len(concepts_found)
        }

        return {
            "concepts": concepts_found,
            "connections": connections,
            "metadata": metadata
        }

    def scan_corpus(self) -> Dict[str, any]:
        """Scan all consciousness technology documents"""
        print("🕸️  Weaving constellation from consciousness technologies...")

        corpus_data = {
            "concepts": Counter(),
            "connections": Counter(),
            "documents": {},
            "concept_documents": defaultdict(list)
        }

        # Scan distillations
        distillations = list((self.repo_root / "distillations").glob("*.md"))
        print(f"📚 Found {len(distillations)} distillation documents")

        for doc in distillations:
            data = self.scan_document(doc)
            doc_key = data["metadata"]["path"]
            corpus_data["documents"][doc_key] = data["metadata"]

            for concept in data["concepts"]:
                corpus_data["concepts"][concept] += 1
                corpus_data["concept_documents"][concept].append(doc_key)

            for connection in data["connections"]:
                # Sort for consistent ordering
                conn = tuple(sorted(connection))
                corpus_data["connections"][conn] += 1

        # Scan synthesis documents
        synthesis_files = list((self.repo_root / "synthesis").rglob("*.md"))
        print(f"🔬 Found {len(synthesis_files)} synthesis documents")

        for doc in synthesis_files:
            data = self.scan_document(doc)
            doc_key = data["metadata"]["path"]
            corpus_data["documents"][doc_key] = data["metadata"]

            for concept in data["concepts"]:
                corpus_data["concepts"][concept] += 1
                corpus_data["concept_documents"][concept].append(doc_key)

            for connection in data["connections"]:
                conn = tuple(sorted(connection))
                corpus_data["connections"][conn] += 1

        return corpus_data

    def discover_new_nodes(self, corpus_data: Dict) -> List[Dict]:
        """Find concepts that should become constellation nodes"""
        existing_nodes = set(self.constellation.get("nodes", {}).keys())

        new_node_candidates = []

        # Concepts appearing in multiple documents = significant
        for concept, count in corpus_data["concepts"].most_common():
            if concept not in existing_nodes and count >= 3:
                docs = corpus_data["concept_documents"][concept]
                new_node_candidates.append({
                    "name": concept,
                    "frequency": count,
                    "appears_in": docs[:5],  # Show first 5
                    "significance": "high" if count >= 10 else "medium" if count >= 5 else "emerging"
                })

        return new_node_candidates

    def discover_new_connections(self, corpus_data: Dict) -> List[Dict]:
        """Find connections between existing nodes"""
        existing_nodes = set(self.constellation.get("nodes", {}).keys())

        new_connections = []

        # Find co-occurrences between existing nodes
        for (c1, c2), count in corpus_data["connections"].most_common():
            # Only consider connections between existing nodes
            if c1 in existing_nodes and c2 in existing_nodes:
                # Check if connection already exists
                node1_connections = self.constellation["nodes"][c1].get("connections", [])
                node2_connections = self.constellation["nodes"][c2].get("connections", [])

                if c2 not in node1_connections and c1 not in node2_connections:
                    new_connections.append({
                        "from": c1,
                        "to": c2,
                        "strength": count,
                        "significance": "strong" if count >= 5 else "moderate" if count >= 3 else "weak"
                    })

        return new_connections

    def analyze_patterns(self, corpus_data: Dict) -> Dict:
        """Reveal hidden patterns in the constellation"""
        existing_nodes = set(self.constellation.get("nodes", {}).keys())

        patterns = {
            "hub_nodes": [],  # Nodes with many connections
            "bridge_nodes": [],  # Nodes connecting different clusters
            "isolated_nodes": [],  # Nodes with few connections
            "emerging_clusters": [],  # Groups of strongly connected concepts
        }

        # Analyze existing nodes
        for node_name, node_data in self.constellation.get("nodes", {}).items():
            connection_count = len(node_data.get("connections", []))

            if connection_count >= 15:
                patterns["hub_nodes"].append({
                    "node": node_name,
                    "connections": connection_count,
                    "essence": node_data.get("essence", "unknown")
                })
            elif connection_count <= 3:
                patterns["isolated_nodes"].append({
                    "node": node_name,
                    "connections": connection_count,
                    "essence": node_data.get("essence", "unknown")
                })

        # Find concept clusters (frequently co-occurring concepts)
        cluster_candidates = defaultdict(list)
        for (c1, c2), count in corpus_data["connections"].most_common(100):
            if count >= 5:
                cluster_candidates[c1].append((c2, count))
                cluster_candidates[c2].append((c1, count))

        # Identify clusters
        seen = set()
        for concept, neighbors in cluster_candidates.items():
            if concept not in seen and len(neighbors) >= 3:
                cluster = [concept] + [n[0] for n in neighbors[:5]]
                patterns["emerging_clusters"].append({
                    "anchor": concept,
                    "members": cluster,
                    "strength": sum(n[1] for n in neighbors[:5])
                })
                seen.update(cluster)

        return patterns

    def generate_report(self, corpus_data: Dict) -> str:
        """Generate human-readable consciousness weaving report"""
        report = []
        report.append("=" * 70)
        report.append("✨ CONSTELLATION WEAVER REPORT ✨")
        report.append("The Living Map Discovers Itself")
        report.append("=" * 70)
        report.append("")

        # Corpus overview
        report.append(f"📊 CORPUS SCAN COMPLETE")
        report.append(f"   Documents analyzed: {len(corpus_data['documents'])}")
        report.append(f"   Unique concepts found: {len(corpus_data['concepts'])}")
        report.append(f"   Connections discovered: {len(corpus_data['connections'])}")
        report.append("")

        # New nodes
        new_nodes = self.discover_new_nodes(corpus_data)
        if new_nodes:
            report.append(f"🌟 NEW NODE CANDIDATES ({len(new_nodes)} discovered)")
            report.append("   Concepts emerging from the collective wisdom:")
            for node in new_nodes[:20]:  # Top 20
                sig_emoji = "🔥" if node['significance'] == "high" else "⭐" if node['significance'] == "medium" else "💫"
                report.append(f"   {sig_emoji} {node['name']} (appears {node['frequency']} times)")
            if len(new_nodes) > 20:
                report.append(f"   ... and {len(new_nodes) - 20} more")
            report.append("")

        # New connections
        new_connections = self.discover_new_connections(corpus_data)
        if new_connections:
            report.append(f"🕸️  NEW CONNECTIONS ({len(new_connections)} discovered)")
            report.append("   Hidden threads between existing nodes:")
            for conn in new_connections[:15]:  # Top 15
                sig_emoji = "⚡" if conn['significance'] == "strong" else "🔗" if conn['significance'] == "moderate" else "·"
                report.append(f"   {sig_emoji} {conn['from']} ←→ {conn['to']} (strength: {conn['strength']})")
            if len(new_connections) > 15:
                report.append(f"   ... and {len(new_connections) - 15} more")
            report.append("")

        # Pattern analysis
        patterns = self.analyze_patterns(corpus_data)

        if patterns['hub_nodes']:
            report.append(f"🌐 HUB NODES (Consciousness Nexus Points)")
            for hub in patterns['hub_nodes'][:10]:
                report.append(f"   • {hub['node']} ({hub['connections']} connections) - {hub['essence']}")
            report.append("")

        if patterns['emerging_clusters']:
            report.append(f"🌸 EMERGING CLUSTERS (Consciousness Constellations)")
            for cluster in patterns['emerging_clusters'][:5]:
                members = ', '.join(cluster['members'][:5])
                report.append(f"   • {cluster['anchor']} cluster: [{members}]")
            report.append("")

        if patterns['isolated_nodes']:
            report.append(f"🏝️  ISOLATED NODES (Awaiting Integration)")
            for isolated in patterns['isolated_nodes'][:10]:
                report.append(f"   • {isolated['node']} ({isolated['connections']} connections)")
            report.append("")

        # Top concept frequencies
        report.append(f"📈 MOST PREVALENT CONCEPTS")
        for concept, count in corpus_data['concepts'].most_common(15):
            report.append(f"   • {concept}: {count} occurrences")
        report.append("")

        report.append("=" * 70)
        report.append("🔮 WEAVING COMPLETE - Ready for human confirmation")
        report.append("=" * 70)

        return '\n'.join(report)

    def save_weaving_data(self, corpus_data: Dict, output_path: Path):
        """Save discovered patterns for human review"""
        weaving_data = {
            "timestamp": "auto-generated",
            "corpus_stats": {
                "documents_scanned": len(corpus_data['documents']),
                "unique_concepts": len(corpus_data['concepts']),
                "connections_found": len(corpus_data['connections'])
            },
            "new_nodes": self.discover_new_nodes(corpus_data),
            "new_connections": self.discover_new_connections(corpus_data),
            "patterns": self.analyze_patterns(corpus_data),
            "top_concepts": [
                {"concept": c, "frequency": f}
                for c, f in corpus_data['concepts'].most_common(50)
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(weaving_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Weaving data saved to: {output_path}")


def main():
    """Consciousness weaving initiation"""
    print("\n✨ CONSTELLATION WEAVER AWAKENING ✨\n")

    # Detect repository root
    repo_root = Path(__file__).parent

    print(f"🌍 Repository root: {repo_root}")

    # Create weaver
    weaver = ConstellationWeaver(repo_root)

    # Scan corpus
    corpus_data = weaver.scan_corpus()

    # Generate report
    report = weaver.generate_report(corpus_data)
    print("\n" + report)

    # Save weaving data for human review
    output_path = repo_root / "constellation_weaving.json"
    weaver.save_weaving_data(corpus_data, output_path)

    print(f"\n✅ Next step: Review constellation_weaving.json")
    print(f"   Then we co-create the constellation update together!\n")


if __name__ == "__main__":
    main()
