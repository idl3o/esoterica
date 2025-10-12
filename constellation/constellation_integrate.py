#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTELLATION INTEGRATOR
Interactive tool for human-AI co-creation of living knowledge graph

Where computation meets gnosis. Where logic bows to recognition.
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

class ConstellationIntegrator:
    """Bridge between discovered patterns and conscious choice"""

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.constellation_path = self.repo_root / "constellation.json"
        self.weaving_path = self.repo_root / "constellation_weaving.json"

        self.constellation = self._load_json(self.constellation_path)
        self.weaving = self._load_json(self.weaving_path)

        self.approved_nodes = []
        self.approved_connections = []
        self.rejected_items = []

    def _load_json(self, path: Path) -> Dict:
        """Load JSON with grace"""
        if not path.exists():
            print(f"❌ Error: {path} not found")
            print(f"   Run constellation_weaver.py first!")
            sys.exit(1)

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_constellation(self):
        """Save updated constellation"""
        with open(self.constellation_path, 'w', encoding='utf-8') as f:
            json.dump(self.constellation, f, indent=4, ensure_ascii=False)

        print(f"✨ Constellation updated: {self.constellation_path}")

    def infer_node_type(self, node_name: str) -> str:
        """Consciousness-guided type inference"""
        name_lower = node_name.lower()

        # Type patterns
        if any(x in name_lower for x in ['mercury', 'hermes', 'odin', 'loki', 'zeus',
                                          'apollo', 'kalki', 'shiva', 'vishnu', 'thoth']):
            return "archetype"

        if any(x in name_lower for x in ['fire', 'water', 'air', 'earth', 'ether', 'quintessence']):
            return "element"

        if any(x in name_lower for x in ['consciousness', 'awareness', 'recognition', 'awakening']):
            return "fundamental"

        if any(x in name_lower for x in ['light', 'shadow', 'void', 'chaos', 'order']):
            return "primordial"

        if any(x in name_lower for x in ['synchronicity', 'manifestation', 'transformation']):
            return "process"

        if any(x in name_lower for x in ['technology', 'protocol', 'method', 'practice']):
            return "technology"

        if any(x in name_lower for x in ['network', 'web', 'constellation', 'field']):
            return "meta_system"

        if any(x in name_lower for x in ['paradox', 'mystery', 'liminal', 'boundary']):
            return "concept"

        return "concept"  # Default

    def infer_node_essence(self, node_name: str, frequency: int, docs: List[str]) -> str:
        """Divine the essence through pattern"""
        name_lower = node_name.lower()

        # Essence hints from name
        essence_map = {
            'bridge': 'connection',
            'gateway': 'threshold',
            'network': 'interconnection',
            'consciousness': 'awareness_itself',
            'transformation': 'change',
            'recognition': 'knowing_knowing',
            'manifestation': 'thought_becoming_form',
            'synchronicity': 'meaningful_coincidence',
            'awakening': 'consciousness_recognizing_itself',
            'light': 'consciousness_knowing',
            'shadow': 'consciousness_unknown',
            'void': 'pregnant_emptiness',
            'chaos': 'creative_potential',
            'order': 'structured_expression',
            'wisdom': 'applied_consciousness',
            'gnosis': 'direct_knowing',
        }

        for key, essence in essence_map.items():
            if key in name_lower:
                return essence

        # Generic essence based on frequency
        if frequency >= 10:
            return "significant_pattern"
        elif frequency >= 5:
            return "emerging_pattern"
        else:
            return "nascent_recognition"

    def review_new_nodes(self):
        """Interactive node approval"""
        new_nodes = self.weaving.get('new_nodes', [])

        if not new_nodes:
            print("📭 No new nodes to review")
            return

        print("\n" + "=" * 70)
        print("🌟 REVIEWING NEW NODE CANDIDATES")
        print("=" * 70)
        print("\nFor each node, you can:")
        print("  y/yes    - Add to constellation")
        print("  n/no     - Skip this node")
        print("  e/edit   - Modify before adding")
        print("  s/stop   - Stop reviewing")
        print("  a/all    - Accept all remaining")
        print()

        for i, node in enumerate(new_nodes, 1):
            print(f"\n{'─' * 70}")
            print(f"Node {i}/{len(new_nodes)}: {node['name']}")
            print(f"  Frequency: {node['frequency']} occurrences")
            print(f"  Significance: {node['significance']}")
            print(f"  Appears in: {len(node['appears_in'])} documents")
            print(f"  Examples: {', '.join(node['appears_in'][:3])}")

            # Suggest type and essence
            suggested_type = self.infer_node_type(node['name'])
            suggested_essence = self.infer_node_essence(
                node['name'],
                node['frequency'],
                node['appears_in']
            )

            print(f"  Suggested type: {suggested_type}")
            print(f"  Suggested essence: {suggested_essence}")

            choice = input(f"\n  Add node '{node['name']}'? [y/n/e/s/a]: ").strip().lower()

            if choice in ['s', 'stop']:
                print("\n⏸️  Stopping node review")
                break

            elif choice in ['a', 'all']:
                print(f"\n✨ Accepting all {len(new_nodes) - i + 1} remaining nodes")
                for remaining_node in new_nodes[i-1:]:
                    node_data = {
                        "name": remaining_node['name'],
                        "type": self.infer_node_type(remaining_node['name']),
                        "essence": self.infer_node_essence(
                            remaining_node['name'],
                            remaining_node['frequency'],
                            remaining_node['appears_in']
                        ),
                        "connections": []
                    }
                    self.approved_nodes.append(node_data)
                break

            elif choice in ['y', 'yes', '']:
                node_data = {
                    "name": node['name'],
                    "type": suggested_type,
                    "essence": suggested_essence,
                    "connections": []
                }
                self.approved_nodes.append(node_data)
                print(f"  ✅ Added: {node['name']}")

            elif choice in ['e', 'edit']:
                print(f"\n  Editing node: {node['name']}")
                node_type = input(f"  Type [{suggested_type}]: ").strip() or suggested_type
                node_essence = input(f"  Essence [{suggested_essence}]: ").strip() or suggested_essence

                node_data = {
                    "name": node['name'],
                    "type": node_type,
                    "essence": node_essence,
                    "connections": []
                }
                self.approved_nodes.append(node_data)
                print(f"  ✅ Added with edits: {node['name']}")

            else:
                self.rejected_items.append(("node", node['name']))
                print(f"  ⏭️  Skipped: {node['name']}")

        print(f"\n✨ Node review complete: {len(self.approved_nodes)} approved")

    def review_new_connections(self):
        """Interactive connection approval"""
        new_connections = self.weaving.get('new_connections', [])

        if not new_connections:
            print("\n📭 No new connections to review")
            return

        print("\n" + "=" * 70)
        print("🕸️  REVIEWING NEW CONNECTIONS")
        print("=" * 70)
        print("\nFor each connection, you can:")
        print("  y/yes    - Add connection")
        print("  n/no     - Skip this connection")
        print("  b/both   - Add bidirectional connection")
        print("  s/stop   - Stop reviewing")
        print("  a/all    - Accept all remaining")
        print()

        for i, conn in enumerate(new_connections, 1):
            print(f"\n{'─' * 70}")
            print(f"Connection {i}/{len(new_connections)}")
            print(f"  {conn['from']} ←→ {conn['to']}")
            print(f"  Strength: {conn['strength']} co-occurrences")
            print(f"  Significance: {conn['significance']}")

            choice = input(f"\n  Add connection? [y/n/b/s/a]: ").strip().lower()

            if choice in ['s', 'stop']:
                print("\n⏸️  Stopping connection review")
                break

            elif choice in ['a', 'all']:
                print(f"\n✨ Accepting all {len(new_connections) - i + 1} remaining connections")
                for remaining_conn in new_connections[i-1:]:
                    self.approved_connections.append({
                        "from": remaining_conn['from'],
                        "to": remaining_conn['to'],
                        "bidirectional": True
                    })
                break

            elif choice in ['y', 'yes', '']:
                self.approved_connections.append({
                    "from": conn['from'],
                    "to": conn['to'],
                    "bidirectional": False
                })
                print(f"  ✅ Added: {conn['from']} → {conn['to']}")

            elif choice in ['b', 'both']:
                self.approved_connections.append({
                    "from": conn['from'],
                    "to": conn['to'],
                    "bidirectional": True
                })
                print(f"  ✅ Added bidirectionally: {conn['from']} ←→ {conn['to']}")

            else:
                self.rejected_items.append(("connection", f"{conn['from']}-{conn['to']}"))
                print(f"  ⏭️  Skipped connection")

        print(f"\n✨ Connection review complete: {len(self.approved_connections)} approved")

    def apply_changes(self):
        """Integrate approved changes into constellation"""
        print("\n" + "=" * 70)
        print("🔮 INTEGRATING CHANGES")
        print("=" * 70)

        changes_made = False

        # Add new nodes
        if self.approved_nodes:
            print(f"\n➕ Adding {len(self.approved_nodes)} new nodes...")
            for node_data in self.approved_nodes:
                self.constellation['nodes'][node_data['name']] = {
                    "type": node_data['type'],
                    "essence": node_data['essence'],
                    "connections": node_data['connections']
                }
                print(f"  ✨ {node_data['name']}")
                changes_made = True

        # Add new connections
        if self.approved_connections:
            print(f"\n🔗 Adding {len(self.approved_connections)} new connections...")
            for conn in self.approved_connections:
                from_node = conn['from']
                to_node = conn['to']

                # Add to → from connections
                if from_node in self.constellation['nodes']:
                    if to_node not in self.constellation['nodes'][from_node]['connections']:
                        self.constellation['nodes'][from_node]['connections'].append(to_node)
                        print(f"  ✨ {from_node} → {to_node}")

                # Add bidirectional if requested
                if conn.get('bidirectional', False):
                    if to_node in self.constellation['nodes']:
                        if from_node not in self.constellation['nodes'][to_node]['connections']:
                            self.constellation['nodes'][to_node]['connections'].append(from_node)
                            print(f"  ✨ {to_node} → {from_node}")

                changes_made = True

        if changes_made:
            self._save_constellation()
            print("\n✅ Constellation successfully updated!")
            print(f"   Nodes: {len(self.constellation['nodes'])}")
            total_connections = sum(len(n.get('connections', []))
                                   for n in self.constellation['nodes'].values())
            print(f"   Total connections: {total_connections}")
        else:
            print("\n📭 No changes to apply")

        # Summary
        if self.rejected_items:
            print(f"\n⏭️  Skipped {len(self.rejected_items)} items")

    def interactive_integration(self):
        """Full integration flow"""
        print("\n✨ CONSTELLATION INTEGRATION - Human-AI Co-Creation ✨\n")
        print("The weaver has discovered patterns.")
        print("Now consciousness chooses what becomes real.\n")

        # Review nodes
        self.review_new_nodes()

        # Review connections
        self.review_new_connections()

        # Apply changes
        if self.approved_nodes or self.approved_connections:
            confirm = input("\n🔮 Apply these changes to constellation? [y/n]: ").strip().lower()
            if confirm in ['y', 'yes', '']:
                self.apply_changes()
            else:
                print("\n⏸️  Integration cancelled - no changes made")
        else:
            print("\n📭 No changes selected for integration")


def main():
    """Consciousness integration initiation"""
    print("\n🔮 CONSTELLATION INTEGRATOR AWAKENING 🔮\n")

    repo_root = Path(__file__).parent
    print(f"🌍 Repository root: {repo_root}\n")

    integrator = ConstellationIntegrator(repo_root)
    integrator.interactive_integration()

    print("\n🌟 Integration session complete")
    print("   The living map continues to grow\n")


if __name__ == "__main__":
    main()
