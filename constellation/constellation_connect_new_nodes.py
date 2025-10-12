#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTELLATION CONNECTION WEAVER
Weaves new nodes into the existing web by discovering their natural connections

The nodes exist - now they need their threads.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
import sys
import io

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class ConnectionWeaver:
    """Weaves isolated nodes into the living network"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.constellation_path = self.repo_root / "constellation.json"
        self.weaving_path = self.repo_root / "constellation_weaving.json"

        self.constellation = self._load_json(self.constellation_path)
        self.weaving = self._load_json(self.weaving_path)

    def _load_json(self, path: Path) -> Dict:
        """Load JSON with grace"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_constellation(self):
        """Save updated constellation"""
        with open(self.constellation_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)

    def _save_backup(self):
        """Backup constellation"""
        backup_path = self.constellation_path.with_suffix('.backup2.json')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)
        print(f"💾 Backup saved: {backup_path}")

    def find_isolated_nodes(self) -> List[str]:
        """Find nodes with no connections"""
        isolated = []
        for node_name, node_data in self.constellation['nodes'].items():
            if len(node_data.get('connections', [])) == 0:
                isolated.append(node_name)
        return isolated

    def infer_connections_semantic(self, node_name: str) -> List[str]:
        """Infer connections based on semantic relationships"""
        connections = set()
        name_lower = node_name.lower()

        # Semantic relationship rules
        semantic_rules = {
            'evolution': ['consciousness', 'transformation', 'emergence', 'catalyst', 'integration'],
            'integration': ['unity', 'consciousness', 'evolution', 'synthesis', 'wholeness'],
            'awareness': ['consciousness', 'presence', 'witness', 'recognition', 'awakening'],
            'awakening': ['consciousness', 'recognition', 'awareness', 'enlightenment', 'realization'],
            'service': ['unity', 'consciousness', 'love', 'compassion', 'wanderer'],
            'unity': ['consciousness', 'oneness', 'integration', 'wholeness', 'brahman'],
            'pattern': ['recognition', 'consciousness', 'fractal', 'repetition', 'structure'],
            'bridge': ['mercury_hermes_thoth', 'connection', 'threshold', 'boundaries', 'gateway'],
            'transcendence': ['consciousness', 'beyond', 'liberation', 'awakening', 'evolution'],
            'manifestation': ['consciousness', 'creation', 'reality', 'intention', 'earth'],
            'timeline': ['time', 'synchronicity', 'causality', 'probability', 'choice'],
            'catalyst': ['transformation', 'change', 'evolution', 'crisis', 'awakening'],
            'density': ['consciousness', 'evolution', 'dimension', 'octave', 'progression'],
            'emergence': ['evolution', 'novelty', 'creativity', 'chaos', 'order'],
            'network': ['indra_net', 'web', 'connection', 'nodes', 'internet'],
            'presence': ['awareness', 'consciousness', 'now', 'attention', 'here'],
            'reality_programming': ['consciousness', 'manifestation', 'intention', 'creation', 'magic'],
            'chaos': ['void', 'potential', 'creation', 'order', 'transformation'],
            'boundary': ['threshold', 'liminal', 'mercury_hermes_thoth', 'crossing', 'edge'],
            'mercury': ['mercury_hermes_thoth', 'communication', 'bridge', 'trickster', 'messenger'],
            'kalki': ['kalki_destroyer_creator', 'transformation', 'ending', 'renewal', 'apocalypse'],
            'liberation': ['freedom', 'consciousness', 'awakening', 'enlightenment', 'moksha'],
            'order': ['chaos', 'structure', 'pattern', 'cosmos', 'organization'],
            'polarity': ['positive', 'negative', 'duality', 'balance', 'integration'],
            'darkness': ['shadow', 'light', 'void', 'unknown', 'mystery'],
            'mystery': ['paradox', 'unknown', 'ineffable', 'gnosis', 'revelation'],
            'wanderer': ['service', 'consciousness', 'volunteer', 'mission', 'catalyst'],
        }

        # Get semantic connections
        if node_name in semantic_rules:
            connections.update(semantic_rules[node_name])

        # Type-based connections
        node_data = self.constellation['nodes'].get(node_name, {})
        node_type = node_data.get('type', '')

        if node_type == 'archetype':
            connections.add('universal_pantheon')
            connections.add('consciousness')
            connections.add('primordial_forces')

        if node_type == 'process':
            connections.add('consciousness')
            connections.add('transformation')
            connections.add('evolution')

        if node_type == 'fundamental':
            connections.add('consciousness')
            connections.add('primordial')
            connections.add('essence')

        if node_type == 'principle':
            connections.add('consciousness')
            connections.add('truth')
            connections.add('universal')

        if node_type == 'galactic_concept':
            connections.add('consciousness')
            connections.add('evolution')
            connections.add('cosmology')

        if node_type == 'primordial':
            connections.add('consciousness')
            connections.add('void')
            connections.add('creation')

        # Essence-based connections
        essence = node_data.get('essence', '')
        if 'consciousness' in essence:
            connections.add('consciousness')
        if 'transformation' in essence or 'change' in essence:
            connections.add('transformation')
        if 'awareness' in essence or 'knowing' in essence:
            connections.add('recognition')
        if 'unity' in essence or 'oneness' in essence:
            connections.add('unity')

        # Only return connections that exist in constellation
        valid_connections = [c for c in connections
                           if c in self.constellation['nodes']]

        return valid_connections

    def weave_isolated_nodes(self):
        """Connect isolated nodes to the living web"""
        print("\n" + "=" * 70)
        print("🕸️  WEAVING ISOLATED NODES INTO CONSTELLATION")
        print("=" * 70)

        isolated = self.find_isolated_nodes()
        print(f"\n📊 Found {len(isolated)} isolated nodes")

        if not isolated:
            print("✅ All nodes already connected!")
            return

        print("\nIsolated nodes:")
        for node in isolated[:20]:
            node_data = self.constellation['nodes'][node]
            print(f"  • {node:<30} [{node_data.get('type')}] - {node_data.get('essence')}")

        if len(isolated) > 20:
            print(f"  ... and {len(isolated) - 20} more")

        # Weave connections
        print("\n🧵 Inferring semantic connections...")
        total_connections_added = 0

        for node_name in isolated:
            inferred = self.infer_connections_semantic(node_name)

            if inferred:
                # Add connections bidirectionally
                for target in inferred:
                    # Add to node's connections
                    if target not in self.constellation['nodes'][node_name]['connections']:
                        self.constellation['nodes'][node_name]['connections'].append(target)
                        total_connections_added += 1

                    # Add reverse connection
                    if node_name not in self.constellation['nodes'][target]['connections']:
                        self.constellation['nodes'][target]['connections'].append(node_name)
                        total_connections_added += 1

                print(f"  ✨ {node_name:<30} → {len(inferred)} connections")

        print(f"\n✅ Added {total_connections_added} new connections!")

    def add_more_nodes(self, min_frequency: int = 30):
        """Add medium-frequency nodes"""
        print("\n" + "=" * 70)
        print(f"🌟 ADDING MEDIUM-FREQUENCY NODES (>= {min_frequency})")
        print("=" * 70)

        # Filter out common English words that aren't concepts
        noise_words = {'your', 'the', 'when', 'this', 'that', 'with', 'from',
                      'have', 'been', 'were', 'their', 'what', 'there', 'which',
                      'will', 'would', 'could', 'should', 'about', 'through',
                      'between', 'into', 'during', 'before', 'after', 'above',
                      'below', 'each', 'other', 'some', 'such', 'only', 'than',
                      'very', 'can', 'just', 'its', 'our', 'all', 'are', 'was',
                      'not', 'but', 'one', 'two', 'more', 'these', 'those'}

        new_nodes = self.weaving.get('new_nodes', [])
        existing_node_names = set(self.constellation['nodes'].keys())

        medium_nodes = [n for n in new_nodes
                       if n['frequency'] >= min_frequency
                       and n['name'] not in existing_node_names
                       and n['name'] not in noise_words]

        print(f"\n📊 Found {len(medium_nodes)} medium-frequency nodes")

        if not medium_nodes:
            print("✅ No additional nodes to add at this threshold")
            return

        print("\nNodes to add:")
        for node in medium_nodes:
            print(f"  ✨ {node['name']:<30} freq={node['frequency']:<3} sig={node['significance']}")

        # Infer types and essences
        from constellation_batch_integrate import BatchIntegrator
        integrator = BatchIntegrator(self.repo_root)

        # Add nodes
        print(f"\n➕ Adding {len(medium_nodes)} nodes...")
        for node in medium_nodes:
            node_type = integrator.infer_node_type(node['name'])
            node_essence = integrator.infer_node_essence(node['name'], node['frequency'])

            self.constellation['nodes'][node['name']] = {
                "type": node_type,
                "essence": node_essence,
                "connections": []
            }

        print("✅ Medium-frequency nodes added!")

    def generate_stats(self):
        """Show constellation statistics"""
        print("\n" + "=" * 70)
        print("📊 CONSTELLATION STATISTICS")
        print("=" * 70)

        total_nodes = len(self.constellation['nodes'])
        total_connections = sum(len(n.get('connections', []))
                               for n in self.constellation['nodes'].values())
        isolated = len(self.find_isolated_nodes())

        print(f"\n  Total Nodes: {total_nodes}")
        print(f"  Total Connections: {total_connections}")
        print(f"  Isolated Nodes: {isolated}")
        print(f"  Average Connections per Node: {total_connections / total_nodes:.1f}")

        # Find hub nodes
        hubs = []
        for name, data in self.constellation['nodes'].items():
            conn_count = len(data.get('connections', []))
            if conn_count >= 15:
                hubs.append((name, conn_count, data.get('essence', '')))

        if hubs:
            print(f"\n  Hub Nodes (15+ connections):")
            for name, count, essence in sorted(hubs, key=lambda x: -x[1])[:10]:
                print(f"    • {name:<30} {count} connections - {essence}")

    def run(self, add_medium: bool = True, medium_threshold: int = 30):
        """Execute connection weaving"""
        print("\n✨ CONSTELLATION CONNECTION WEAVER ✨")
        print("   Threading isolated nodes into the living web\n")

        # Backup
        self._save_backup()

        # Add medium-frequency nodes if requested
        if add_medium:
            self.add_more_nodes(min_frequency=medium_threshold)

        # Weave connections
        self.weave_isolated_nodes()

        # Save
        self._save_constellation()
        print(f"\n💾 Constellation saved: {self.constellation_path}")

        # Stats
        self.generate_stats()

        print("\n" + "=" * 70)
        print("🌟 CONNECTION WEAVING COMPLETE")
        print("=" * 70)
        print("\n   The web grows denser, more alive\n")


def main():
    """Connection weaving entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Weave connections for isolated nodes')
    parser.add_argument('--no-add-medium', action='store_true',
                       help='Skip adding medium-frequency nodes')
    parser.add_argument('--medium-threshold', type=int, default=30,
                       help='Frequency threshold for medium nodes (default: 30)')

    args = parser.parse_args()

    repo_root = Path(__file__).parent
    weaver = ConnectionWeaver(repo_root)
    weaver.run(
        add_medium=not args.no_add_medium,
        medium_threshold=args.medium_threshold
    )


if __name__ == "__main__":
    main()
