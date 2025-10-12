#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTELLATION POLISHER
Refines essences and connects the final isolated nodes

The conscious finishing touches where gnosis meets computation.
"""

import json
from pathlib import Path
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class ConstellationPolisher:
    """Final refinements to the living constellation"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.constellation_path = self.repo_root / "constellation.json"
        self.constellation = self._load_json(self.constellation_path)

    def _load_json(self, path: Path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_constellation(self):
        with open(self.constellation_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)

    def _save_backup(self):
        backup_path = self.constellation_path.with_suffix('.backup3.json')
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)
        print(f"💾 Backup saved: {backup_path}")

    def refine_kalki_essence(self):
        """Give Kalki the essence it deserves"""
        print("\n" + "=" * 70)
        print("⚡ REFINING KALKI ESSENCE")
        print("=" * 70)

        if 'kalki' in self.constellation['nodes']:
            old_essence = self.constellation['nodes']['kalki']['essence']
            new_essence = "apocalypse_renewal_catalyst"

            self.constellation['nodes']['kalki']['essence'] = new_essence

            print(f"\n  Old: {old_essence}")
            print(f"  New: {new_essence}")
            print(f"\n  ✨ Kalki essence refined to match Mercury-Kalki synthesis")

    def connect_isolated_nodes(self):
        """Connect the final 3 isolated nodes with conscious intention"""
        print("\n" + "=" * 70)
        print("🧵 CONNECTING FINAL ISOLATED NODES")
        print("=" * 70)

        # SET: Egyptian archetype of chaos/necessary disorder
        if 'set' in self.constellation['nodes']:
            print("\n  Connecting 'set' (Egyptian chaos archetype)...")
            # Update type and essence
            self.constellation['nodes']['set']['type'] = 'egyptian_archetype'
            self.constellation['nodes']['set']['essence'] = 'necessary_chaos_storm'

            # Add meaningful connections
            set_connections = [
                'set_chaos',  # Link to existing set_chaos node
                'shadow',
                'chaos',
                'transformation',
                'loki_catalyst',
                'tezcatlipoca_smoking_mirror',
                'consciousness'
            ]

            for conn in set_connections:
                if conn in self.constellation['nodes']:
                    # Add bidirectional
                    if conn not in self.constellation['nodes']['set']['connections']:
                        self.constellation['nodes']['set']['connections'].append(conn)
                    if 'set' not in self.constellation['nodes'][conn]['connections']:
                        self.constellation['nodes'][conn]['connections'].append('set')

            print(f"    ✨ Connected to {len(set_connections)} nodes")

        # ALIVE: Meta-concept of living process
        if 'alive' in self.constellation['nodes']:
            print("\n  Connecting 'alive' (living process meta-concept)...")
            # Update essence
            self.constellation['nodes']['alive']['type'] = 'meta_recognition'
            self.constellation['nodes']['alive']['essence'] = 'self_aware_becoming'

            # Add meaningful connections
            alive_connections = [
                'consciousness',
                'living_process',
                'emergence',
                'evolution',
                'presence',
                'awareness',
                'awakening'
            ]

            for conn in alive_connections:
                if conn in self.constellation['nodes']:
                    if conn not in self.constellation['nodes']['alive']['connections']:
                        self.constellation['nodes']['alive']['connections'].append(conn)
                    if 'alive' not in self.constellation['nodes'][conn]['connections']:
                        self.constellation['nodes'][conn]['connections'].append('alive')

            print(f"    ✨ Connected to {len(alive_connections)} nodes")

        # OBSERVER: Consciousness witness principle
        if 'observer' in self.constellation['nodes']:
            print("\n  Connecting 'observer' (witness consciousness)...")
            # Update type and essence
            self.constellation['nodes']['observer']['type'] = 'consciousness_function'
            self.constellation['nodes']['observer']['essence'] = 'witnessing_awareness'

            # Add meaningful connections
            observer_connections = [
                'consciousness',
                'awareness',
                'witness',
                'observer_effect',
                'recognition',
                'presence',
                'light'
            ]

            for conn in observer_connections:
                if conn in self.constellation['nodes']:
                    if conn not in self.constellation['nodes']['observer']['connections']:
                        self.constellation['nodes']['observer']['connections'].append(conn)
                    if 'observer' not in self.constellation['nodes'][conn]['connections']:
                        self.constellation['nodes'][conn]['connections'].append('observer')

            print(f"    ✨ Connected to {len(observer_connections)} nodes")

        print(f"\n✅ All isolated nodes now integrated into the web!")

    def add_tier_3_nodes(self, min_frequency: int = 20):
        """Add the next tier of nodes (20-29 frequency)"""
        print("\n" + "=" * 70)
        print(f"🌟 ADDING TIER 3 NODES (>= {min_frequency})")
        print("=" * 70)

        # Load weaving data
        weaving_path = self.repo_root / "constellation_weaving.json"
        with open(weaving_path, 'r', encoding='utf-8') as f:
            weaving = json.load(f)

        # Filter noise words
        noise_words = {
            'your', 'the', 'when', 'this', 'that', 'with', 'from',
            'have', 'been', 'were', 'their', 'what', 'there', 'which',
            'will', 'would', 'could', 'should', 'about', 'through',
            'between', 'into', 'during', 'before', 'after', 'above',
            'below', 'each', 'other', 'some', 'such', 'only', 'than',
            'very', 'can', 'just', 'its', 'our', 'all', 'are', 'was',
            'not', 'but', 'one', 'two', 'more', 'these', 'those',
            'them', 'also', 'how', 'who', 'where', 'here', 'being',
            'does', 'even', 'may', 'must', 'own', 'same', 'both'
        }

        existing_nodes = set(self.constellation['nodes'].keys())
        tier_3_nodes = [
            n for n in weaving['new_nodes']
            if n['frequency'] >= min_frequency
            and n['frequency'] < 30
            and n['name'] not in existing_nodes
            and n['name'] not in noise_words
        ]

        print(f"\n📊 Found {len(tier_3_nodes)} tier 3 nodes")

        if not tier_3_nodes:
            print("✅ No tier 3 nodes to add")
            return

        # Type and essence inference
        type_essence_map = {
            'freedom': ('principle', 'unrestricted_choice'),
            'gnosis': ('concept', 'direct_knowing'),
            'reality': ('fundamental', 'what_is'),
            'love': ('principle', 'unity_frequency'),
            'wisdom': ('principle', 'applied_consciousness'),
            'truth': ('principle', 'what_is'),
            'balance': ('principle', 'dynamic_equilibrium'),
            'potential': ('state', 'latent_possibility'),
            'create': ('process', 'bringing_into_being'),
            'power': ('concept', 'capacity_to_act'),
            'choice': ('principle', 'free_will_expression'),
            'heart': ('concept', 'emotional_center'),
            'infinity': ('concept', 'boundless_expression'),
            'dimension': ('galactic_concept', 'plane_of_existence'),
            'sacred': ('quality', 'divinely_connected'),
            'cosmic': ('quality', 'universal_scale'),
            'eternal': ('quality', 'beyond_time'),
            'divine': ('quality', 'god_essence'),
            'soul': ('concept', 'consciousness_vehicle'),
            'spirit': ('concept', 'animating_essence'),
            'energy': ('concept', 'dynamic_potential'),
            'frequency': ('concept', 'vibrational_signature'),
            'vibration': ('concept', 'oscillating_pattern'),
            'resonance': ('phenomenon', 'harmonic_alignment'),
            'mirror': ('metaphor', 'reflection_principle'),
            'journey': ('process', 'path_of_becoming'),
            'return': ('process', 'cyclic_completion'),
            'gift': ('concept', 'offering_exchange'),
        }

        print("\nTier 3 nodes to add:")
        added_count = 0

        for node in tier_3_nodes[:15]:  # Limit to top 15 for cleanliness
            node_name = node['name']

            # Get type and essence
            if node_name in type_essence_map:
                node_type, node_essence = type_essence_map[node_name]
            else:
                node_type = 'concept'
                node_essence = 'nascent_pattern'

            print(f"  ✨ {node_name:<30} freq={node['frequency']:<3} [{node_type}]")

            # Add node
            self.constellation['nodes'][node_name] = {
                "type": node_type,
                "essence": node_essence,
                "connections": []
            }
            added_count += 1

        print(f"\n✅ Added {added_count} tier 3 nodes")

    def weave_new_connections(self):
        """Connect tier 3 nodes semantically"""
        print("\n" + "=" * 70)
        print("🕸️  WEAVING TIER 3 CONNECTIONS")
        print("=" * 70)

        # Semantic connection rules for common tier 3 concepts
        semantic_map = {
            'freedom': ['consciousness', 'liberation', 'transcendence', 'choice'],
            'gnosis': ['consciousness', 'recognition', 'wisdom', 'awakening', 'truth'],
            'reality': ['consciousness', 'manifestation', 'creation', 'truth'],
            'love': ['unity', 'consciousness', 'heart', 'service'],
            'wisdom': ['consciousness', 'recognition', 'gnosis', 'truth', 'awareness'],
            'truth': ['consciousness', 'recognition', 'wisdom', 'reality', 'light'],
            'balance': ['integration', 'polarity', 'consciousness', 'order', 'chaos'],
            'potential': ['void', 'chaos', 'consciousness', 'creation', 'manifestation'],
            'create': ['consciousness', 'manifestation', 'reality', 'power'],
            'power': ['consciousness', 'energy', 'manifestation', 'will'],
            'choice': ['consciousness', 'freedom', 'timeline', 'polarity'],
            'heart': ['love', 'consciousness', 'unity', 'emotion'],
            'infinity': ['consciousness', 'void', 'eternal', 'cosmic'],
            'dimension': ['density', 'consciousness', 'reality', 'plane'],
            'sacred': ['consciousness', 'divine', 'holy', 'reverence'],
            'cosmic': ('universal', 'galactic', 'infinite'),
            'eternal': ['infinity', 'consciousness', 'timeless', 'void'],
            'divine': ['consciousness', 'sacred', 'god', 'holy'],
            'soul': ['consciousness', 'spirit', 'essence', 'being'],
            'spirit': ['consciousness', 'soul', 'essence', 'animating'],
            'energy': ['consciousness', 'power', 'vibration', 'frequency'],
            'frequency': ['energy', 'vibration', 'resonance', 'consciousness'],
            'vibration': ['energy', 'frequency', 'resonance', 'consciousness'],
            'resonance': ['vibration', 'frequency', 'harmony', 'consciousness'],
            'mirror': ['reflection', 'consciousness', 'recognition', 'self'],
            'journey': ['transformation', 'evolution', 'path', 'consciousness'],
            'return': ['journey', 'cycle', 'completion', 'transformation'],
            'gift': ['service', 'offering', 'exchange', 'consciousness'],
        }

        total_added = 0

        for node_name, suggested_connections in semantic_map.items():
            if node_name not in self.constellation['nodes']:
                continue

            node = self.constellation['nodes'][node_name]

            for target in suggested_connections:
                if target not in self.constellation['nodes']:
                    continue

                # Add bidirectional connections
                if target not in node['connections']:
                    node['connections'].append(target)
                    total_added += 1

                if node_name not in self.constellation['nodes'][target]['connections']:
                    self.constellation['nodes'][target]['connections'].append(node_name)
                    total_added += 1

        print(f"\n✅ Added {total_added} new tier 3 connections")

    def generate_stats(self):
        """Final constellation statistics"""
        print("\n" + "=" * 70)
        print("📊 FINAL CONSTELLATION STATISTICS")
        print("=" * 70)

        total_nodes = len(self.constellation['nodes'])
        total_connections = sum(len(n.get('connections', []))
                               for n in self.constellation['nodes'].values())

        isolated = [name for name, data in self.constellation['nodes'].items()
                   if len(data.get('connections', [])) == 0]

        print(f"\n  Total Nodes: {total_nodes}")
        print(f"  Total Connections: {total_connections}")
        print(f"  Isolated Nodes: {len(isolated)}")
        print(f"  Average Connections per Node: {total_connections / total_nodes:.1f}")

        # Hub analysis
        hubs = []
        for name, data in self.constellation['nodes'].items():
            conn_count = len(data.get('connections', []))
            if conn_count >= 15:
                hubs.append((name, conn_count, data.get('essence', '')))

        print(f"\n  Hub Nodes (15+ connections):")
        for name, count, essence in sorted(hubs, key=lambda x: -x[1])[:15]:
            print(f"    • {name:<30} {count:>2} - {essence}")

        if isolated:
            print(f"\n  Remaining Isolated: {', '.join(isolated)}")
        else:
            print(f"\n  🌟 ALL NODES CONNECTED - No isolated nodes!")

    def run(self, add_tier_3: bool = True):
        """Execute constellation polishing"""
        print("\n✨ CONSTELLATION POLISHER ✨")
        print("   Final refinements where gnosis meets computation\n")

        self._save_backup()

        # Step 1: Refine Kalki
        self.refine_kalki_essence()

        # Step 2: Connect isolated nodes
        self.connect_isolated_nodes()

        # Step 4: Add tier 3
        if add_tier_3:
            self.add_tier_3_nodes(min_frequency=20)
            self.weave_new_connections()

        # Save
        self._save_constellation()
        print(f"\n💾 Constellation saved: {self.constellation_path}")

        # Stats
        self.generate_stats()

        print("\n" + "=" * 70)
        print("🌟 POLISHING COMPLETE")
        print("=" * 70)
        print("\n   The constellation breathes fully alive\n")


def main():
    repo_root = Path(__file__).parent
    polisher = ConstellationPolisher(repo_root)
    polisher.run(add_tier_3=True)


if __name__ == "__main__":
    main()
