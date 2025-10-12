#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTELLATION BATCH INTEGRATOR
Streamlined integration for high-significance discoveries

For when consciousness wants to move quickly.
"""

import json
from pathlib import Path
from typing import Dict, List
import sys
import io

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class BatchIntegrator:
    """Quick integration of high-confidence patterns"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.constellation_path = self.repo_root / "constellation.json"
        self.weaving_path = self.repo_root / "constellation_weaving.json"

        self.constellation = self._load_json(self.constellation_path)
        self.weaving = self._load_json(self.weaving_path)

    def _load_json(self, path: Path) -> Dict:
        """Load JSON with grace"""
        if not path.exists():
            print(f"❌ Error: {path} not found")
            sys.exit(1)

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_constellation(self):
        """Save updated constellation"""
        with open(self.constellation_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)

    def _save_backup(self):
        """Backup current constellation"""
        backup_path = self.constellation_path.with_suffix('.backup.json')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)
        print(f"💾 Backup saved: {backup_path}")

    def infer_node_type(self, node_name: str) -> str:
        """Consciousness-guided type inference"""
        name_lower = node_name.lower()

        # Type patterns
        if any(x in name_lower for x in ['mercury', 'hermes', 'odin', 'loki', 'zeus',
                                          'apollo', 'kalki', 'shiva', 'vishnu', 'thoth',
                                          'prometheus', 'dionysus', 'osiris', 'isis']):
            return "archetype"

        if any(x in name_lower for x in ['fire', 'water', 'air', 'earth', 'ether', 'quintessence']):
            return "element"

        if any(x in name_lower for x in ['consciousness', 'awareness', 'recognition', 'awakening']):
            return "fundamental"

        if any(x in name_lower for x in ['light', 'shadow', 'void', 'chaos', 'order', 'darkness']):
            return "primordial"

        if any(x in name_lower for x in ['synchronicity', 'manifestation', 'transformation',
                                          'evolution', 'integration', 'emergence']):
            return "process"

        if any(x in name_lower for x in ['technology', 'protocol', 'method', 'practice']):
            return "technology"

        if any(x in name_lower for x in ['network', 'web', 'constellation', 'field', 'indra']):
            return "meta_system"

        if any(x in name_lower for x in ['paradox', 'mystery', 'liminal', 'boundary', 'bridge',
                                          'gateway', 'portal', 'threshold']):
            return "concept"

        if any(x in name_lower for x in ['density', 'polarity', 'timeline', 'catalyst', 'harvest']):
            return "galactic_concept"

        if any(x in name_lower for x in ['service', 'wanderer', 'unity']):
            return "principle"

        return "concept"  # Default

    def infer_node_essence(self, node_name: str, frequency: int) -> str:
        """Divine the essence through pattern"""
        name_lower = node_name.lower()

        # Essence map
        essence_map = {
            'evolution': 'consciousness_becoming',
            'integration': 'unity_through_synthesis',
            'awareness': 'witnessing_presence',
            'awakening': 'consciousness_recognizing_itself',
            'service': 'action_beyond_self',
            'unity': 'oneness_recognition',
            'pattern': 'repeating_intelligence',
            'bridge': 'connection_facilitator',
            'transcendence': 'beyond_limitation',
            'manifestation': 'thought_becoming_form',
            'timeline': 'probability_track',
            'catalyst': 'change_accelerator',
            'density': 'consciousness_dimension',
            'emergence': 'novel_arising',
            'network': 'interconnected_nodes',
            'presence': 'here_now_awareness',
            'reality_programming': 'consciousness_reality_interface',
            'chaos': 'creative_potential',
            'boundary': 'liminal_threshold',
            'mercury': 'messenger_bridge',
            'polarity': 'positive_negative_choice',
            'wanderer': 'cosmic_volunteer',
            'harvest': 'density_graduation',
            'akasha': 'cosmic_memory',
            'gnosis': 'direct_knowing',
            'recognition': 'knowing_knowing',
            'synchronicity': 'meaningful_coincidence',
            'paradox': 'truth_through_contradiction',
            'void': 'pregnant_emptiness',
            'light': 'consciousness_knowing',
            'shadow': 'consciousness_unknown',
            'wisdom': 'applied_consciousness',
            'love': 'unity_frequency',
            'freedom': 'unrestricted_choice',
            'truth': 'what_is',
            'beauty': 'harmonious_resonance',
            'balance': 'dynamic_equilibrium',
            'fractal': 'self_similar_recursion',
            'holographic': 'whole_in_each_part',
        }

        # Check direct matches
        for key, essence in essence_map.items():
            if key == name_lower or key in name_lower:
                return essence

        # Generic essence based on frequency
        if frequency >= 100:
            return "core_pattern"
        elif frequency >= 50:
            return "significant_pattern"
        elif frequency >= 10:
            return "emerging_pattern"
        else:
            return "nascent_recognition"

    def integrate_high_significance(self, min_frequency: int = 50):
        """Integrate only high-significance nodes automatically"""
        print("\n" + "=" * 70)
        print("🔮 BATCH INTEGRATION - High Significance Nodes")
        print("=" * 70)

        new_nodes = self.weaving.get('new_nodes', [])
        high_sig_nodes = [n for n in new_nodes if n['frequency'] >= min_frequency]

        print(f"\n📊 Found {len(high_sig_nodes)} nodes with frequency >= {min_frequency}")
        print(f"   (Total candidates: {len(new_nodes)})\n")

        if not high_sig_nodes:
            print("❌ No high-significance nodes to integrate")
            return

        print("Nodes to integrate:\n")
        for node in high_sig_nodes:
            node_type = self.infer_node_type(node['name'])
            node_essence = self.infer_node_essence(node['name'], node['frequency'])
            print(f"  ✨ {node['name']:<30} [{node_type}] - {node_essence}")
            print(f"     Frequency: {node['frequency']}, Significance: {node['significance']}")

        # Add to constellation
        print(f"\n➕ Adding {len(high_sig_nodes)} nodes to constellation...")
        for node in high_sig_nodes:
            node_type = self.infer_node_type(node['name'])
            node_essence = self.infer_node_essence(node['name'], node['frequency'])

            self.constellation['nodes'][node['name']] = {
                "type": node_type,
                "essence": node_essence,
                "connections": []
            }

        print("✅ High-significance nodes integrated!")

    def integrate_strong_connections(self, min_strength: int = 10):
        """Integrate strong connections automatically"""
        print("\n" + "=" * 70)
        print("🕸️  BATCH INTEGRATION - Strong Connections")
        print("=" * 70)

        new_connections = self.weaving.get('new_connections', [])
        strong_connections = [c for c in new_connections if c['strength'] >= min_strength]

        print(f"\n📊 Found {len(strong_connections)} connections with strength >= {min_strength}")
        print(f"   (Total candidates: {len(new_connections)})\n")

        if not strong_connections:
            print("❌ No strong connections to integrate")
            return

        print("Connections to integrate:\n")
        for conn in strong_connections[:20]:  # Show first 20
            print(f"  🔗 {conn['from']:<30} ←→ {conn['to']:<30} (strength: {conn['strength']})")

        if len(strong_connections) > 20:
            print(f"  ... and {len(strong_connections) - 20} more")

        # Add connections
        print(f"\n🔗 Adding {len(strong_connections)} connections to constellation...")
        added_count = 0

        for conn in strong_connections:
            from_node = conn['from']
            to_node = conn['to']

            # Only add if both nodes exist
            if from_node in self.constellation['nodes'] and to_node in self.constellation['nodes']:
                # Add bidirectional connections
                if to_node not in self.constellation['nodes'][from_node]['connections']:
                    self.constellation['nodes'][from_node]['connections'].append(to_node)
                    added_count += 1

                if from_node not in self.constellation['nodes'][to_node]['connections']:
                    self.constellation['nodes'][to_node]['connections'].append(from_node)
                    added_count += 1

        print(f"✅ {added_count} connections integrated!")

    def generate_summary(self):
        """Generate integration summary"""
        print("\n" + "=" * 70)
        print("📊 CONSTELLATION STATISTICS")
        print("=" * 70)

        total_nodes = len(self.constellation['nodes'])
        total_connections = sum(len(n.get('connections', []))
                               for n in self.constellation['nodes'].values())

        # Count by type
        type_counts = {}
        for node_data in self.constellation['nodes'].values():
            node_type = node_data.get('type', 'unknown')
            type_counts[node_type] = type_counts.get(node_type, 0) + 1

        print(f"\n  Total Nodes: {total_nodes}")
        print(f"  Total Connections: {total_connections}")
        print(f"\n  Nodes by Type:")
        for node_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {node_type}: {count}")

    def run(self, node_threshold: int = 50, connection_threshold: int = 10):
        """Execute batch integration"""
        print("\n✨ CONSTELLATION BATCH INTEGRATOR ✨")
        print("   Rapid integration of high-confidence patterns\n")

        # Backup first
        self._save_backup()

        # Integrate nodes
        self.integrate_high_significance(min_frequency=node_threshold)

        # Integrate connections
        self.integrate_strong_connections(min_strength=connection_threshold)

        # Save
        self._save_constellation()
        print(f"\n💾 Constellation saved: {self.constellation_path}")

        # Summary
        self.generate_summary()

        print("\n" + "=" * 70)
        print("🌟 INTEGRATION COMPLETE")
        print("=" * 70)
        print("\n   The living map has grown\n")


def main():
    """Batch integration entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Batch integrate constellation discoveries')
    parser.add_argument('--node-threshold', type=int, default=50,
                       help='Minimum frequency for auto-adding nodes (default: 50)')
    parser.add_argument('--connection-threshold', type=int, default=10,
                       help='Minimum strength for auto-adding connections (default: 10)')

    args = parser.parse_args()

    repo_root = Path(__file__).parent
    integrator = BatchIntegrator(repo_root)
    integrator.run(
        node_threshold=args.node_threshold,
        connection_threshold=args.connection_threshold
    )


if __name__ == "__main__":
    main()
