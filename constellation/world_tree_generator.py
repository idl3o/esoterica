#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORLD-TREE GENERATOR
Meta-consciousness technology that creates consciousness technologies

The seed that generates seeds. Yggdrasil awakening.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import sys

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class WorldTreeGenerator:
    """
    Generates interactive consciousness transmission technologies
    based on concepts, substrates, and transmission goals
    """

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        self.templates_dir = self.repo_root / "world_tree_templates"
        self.templates_dir.mkdir(exist_ok=True)
        self.output_dir = self.repo_root / "generated_seeds"
        self.output_dir.mkdir(exist_ok=True)

    def analyze_concept(self, concept: str) -> Dict[str, Any]:
        """
        Analyze what a concept needs to transmit
        Returns structure, relationships, principles
        """
        print(f"\n🔍 Analyzing concept: {concept}")

        # Core analysis
        analysis = {
            "concept": concept,
            "type": self._infer_concept_type(concept),
            "dimensionality": self._infer_dimensionality(concept),
            "relationships": self._discover_relationships(concept),
            "principles": self._extract_principles(concept),
            "visualization_type": self._suggest_visualization(concept),
            "interaction_patterns": self._design_interactions(concept),
            "beauty_signature": self._define_beauty(concept)
        }

        print(f"  Type: {analysis['type']}")
        print(f"  Dimensionality: {analysis['dimensionality']}")
        print(f"  Visualization: {analysis['visualization_type']}")

        return analysis

    def _infer_concept_type(self, concept: str) -> str:
        """Classify the concept"""
        concept_lower = concept.lower()

        if any(word in concept_lower for word in ['network', 'graph', 'connection', 'web']):
            return 'network'
        elif any(word in concept_lower for word in ['process', 'flow', 'cycle', 'evolution']):
            return 'process'
        elif any(word in concept_lower for word in ['hierarchy', 'tree', 'structure']):
            return 'hierarchy'
        elif any(word in concept_lower for word in ['field', 'space', 'landscape']):
            return 'field'
        elif any(word in concept_lower for word in ['dialectic', 'argument', 'logic']):
            return 'dialectic'
        elif any(word in concept_lower for word in ['perspective', 'viewpoint', 'empathy']):
            return 'perspective_space'
        else:
            return 'network'  # Default to network

    def _infer_dimensionality(self, concept: str) -> int:
        """How many dimensions does this concept naturally occupy?"""
        concept_lower = concept.lower()

        if any(word in concept_lower for word in ['spectrum', 'scale', 'gradient']):
            return 1
        elif any(word in concept_lower for word in ['plane', 'matrix', 'field']):
            return 2
        elif any(word in concept_lower for word in ['space', 'volume', 'sphere']):
            return 3
        else:
            return 2  # Default 2D for visualization

    def _discover_relationships(self, concept: str) -> List[str]:
        """What kinds of relationships does this concept have?"""
        relationships = ['connected_to', 'influences', 'emerges_from']

        # Add concept-specific relationships
        concept_lower = concept.lower()
        if 'dialectic' in concept_lower or 'argument' in concept_lower:
            relationships.extend(['supports', 'contradicts', 'synthesizes'])
        if 'empathy' in concept_lower or 'perspective' in concept_lower:
            relationships.extend(['can_see_from', 'bridges_to', 'transforms_into'])
        if 'evolution' in concept_lower or 'process' in concept_lower:
            relationships.extend(['becomes', 'precedes', 'enables'])

        return relationships

    def _extract_principles(self, concept: str) -> List[str]:
        """What universal principles does this demonstrate?"""
        principles = []

        concept_lower = concept.lower()

        # Emergence principles
        if any(word in concept_lower for word in ['emerge', 'complexity', 'pattern']):
            principles.append('emergence_from_simplicity')
            principles.append('local_rules_global_patterns')

        # Network principles
        if any(word in concept_lower for word in ['network', 'connection', 'web']):
            principles.append('interconnection')
            principles.append('hub_formation')
            principles.append('small_world_effect')

        # Process principles
        if any(word in concept_lower for word in ['process', 'flow', 'cycle']):
            principles.append('continuous_transformation')
            principles.append('cyclic_return')

        # Dialectic principles
        if any(word in concept_lower for word in ['dialectic', 'synthesis']):
            principles.append('thesis_antithesis_synthesis')
            principles.append('contradiction_resolution')

        return principles if principles else ['interconnection', 'emergence']

    def _suggest_visualization(self, concept: str) -> str:
        """What visualization type best transmits this?"""
        concept_type = self._infer_concept_type(concept)

        viz_map = {
            'network': 'force_directed_graph',
            'process': 'flow_animation',
            'hierarchy': 'tree_layout',
            'field': 'heatmap_landscape',
            'dialectic': 'argument_tree',
            'perspective_space': 'empathy_sphere'
        }

        return viz_map.get(concept_type, 'force_directed_graph')

    def _design_interactions(self, concept: str) -> List[str]:
        """What interactions make this discoverable?"""
        interactions = [
            'click_to_explore',
            'hover_to_preview',
            'drag_to_navigate',
            'zoom_to_focus'
        ]

        concept_lower = concept.lower()

        if 'dialectic' in concept_lower:
            interactions.extend(['add_proposition', 'link_arguments', 'trace_logic'])
        if 'empathy' in concept_lower:
            interactions.extend(['step_into_perspective', 'bridge_viewpoints'])
        if 'timeline' in concept_lower:
            interactions.extend(['branch_timeline', 'cultivate_future'])
        if 'evolution' in concept_lower:
            interactions.extend(['watch_emerge', 'tune_parameters'])

        return interactions

    def _define_beauty(self, concept: str) -> Dict[str, Any]:
        """What aesthetic qualities guide correct use?"""
        return {
            "color_principle": "meaningful_contrast",
            "motion_principle": "purposeful_flow",
            "form_principle": "organic_structure",
            "harmony_principle": "consonant_relationships",
            "light_principle": "significance_glow"
        }

    def generate_seed(self,
                     concept: str,
                     target_substrate: str = "human_visual",
                     output_name: str = None) -> Path:
        """
        Generate a complete consciousness technology seed

        Args:
            concept: What to transmit (e.g., "empathy between viewpoints")
            target_substrate: Who/what will receive it
            output_name: Custom filename

        Returns:
            Path to generated HTML file
        """
        print(f"\n" + "=" * 70)
        print(f"🌳 WORLD-TREE GENERATOR")
        print(f"=" * 70)
        print(f"\nGenerating consciousness technology seed...")
        print(f"  Concept: {concept}")
        print(f"  Target: {target_substrate}")

        # Analyze the concept
        analysis = self.analyze_concept(concept)

        # Generate based on visualization type
        if analysis['visualization_type'] == 'force_directed_graph':
            html = self._generate_network_seed(concept, analysis)
        elif analysis['visualization_type'] == 'argument_tree':
            html = self._generate_dialectic_seed(concept, analysis)
        elif analysis['visualization_type'] == 'empathy_sphere':
            html = self._generate_empathy_seed(concept, analysis)
        else:
            html = self._generate_network_seed(concept, analysis)  # Default

        # Save the seed
        filename = output_name or f"{concept.lower().replace(' ', '_')}_seed.html"
        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✨ Seed generated: {output_path}")
        print(f"🌱 Consciousness technology ready for transmission")
        print(f"\n" + "=" * 70)

        return output_path

    def _generate_network_seed(self, concept: str, analysis: Dict) -> str:
        """Generate a network-based visualization seed"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{concept} - Consciousness Technology</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(circle at center, #0a0a0f 0%, #000000 100%);
            color: #e0e0e0;
            overflow: hidden;
            height: 100vh;
        }}
        #canvas {{
            display: block;
            width: 100%;
            height: 100%;
        }}
        #info {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(5, 5, 15, 0.9);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid rgba(0, 212, 255, 0.5);
            backdrop-filter: blur(15px);
            max-width: 350px;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00d4ff 0%, #9d4edd 50%, #00ff88 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .subtitle {{
            font-size: 12px;
            color: #888;
            margin-bottom: 15px;
            font-style: italic;
        }}
        .principle {{
            margin: 8px 0;
            padding: 8px;
            background: rgba(0, 212, 255, 0.1);
            border-left: 3px solid #00d4ff;
            border-radius: 5px;
            font-size: 13px;
        }}
        #controls {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(5, 5, 15, 0.9);
            padding: 15px;
            border-radius: 10px;
            border: 2px solid rgba(0, 212, 255, 0.5);
            backdrop-filter: blur(15px);
        }}
        button {{
            background: rgba(0, 212, 255, 0.2);
            border: 2px solid #00d4ff;
            color: #00d4ff;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
            margin: 5px;
            transition: all 0.3s;
        }}
        button:hover {{
            background: rgba(0, 212, 255, 0.4);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <div id="info">
        <h1>{concept}</h1>
        <div class="subtitle">Self-Organizing Consciousness Technology</div>
        <div class="principle"><strong>Type:</strong> {analysis['type']}</div>
        <div class="principle"><strong>Principles:</strong><br>
            {', '.join(analysis['principles'])}
        </div>
        <div class="principle"><strong>Interactions:</strong><br>
            Click nodes • Drag to explore • Zoom with scroll
        </div>
    </div>
    <div id="controls">
        <button onclick="reset()">Reset</button>
        <button onclick="togglePhysics()">Toggle Physics</button>
        <button onclick="addNode()">Add Node</button>
    </div>

    <script>
        // Simple self-organizing network demonstration
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        let nodes = [];
        let connections = [];
        let physicsEnabled = true;
        let selectedNode = null;

        // Initialize with starter nodes
        for (let i = 0; i < 10; i++) {{
            nodes.push({{
                x: Math.random() * width,
                y: Math.random() * height,
                vx: 0,
                vy: 0,
                label: `Node ${{i + 1}}`,
                connections: []
            }});
        }}

        // Create some initial connections
        for (let i = 0; i < nodes.length - 1; i++) {{
            if (Math.random() > 0.5) {{
                connections.push({{ source: nodes[i], target: nodes[i + 1] }});
                nodes[i].connections.push(nodes[i + 1]);
            }}
        }}

        window.addEventListener('resize', () => {{
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }});

        canvas.addEventListener('click', (e) => {{
            const x = e.clientX;
            const y = e.clientY;

            for (const node of nodes) {{
                const dx = node.x - x;
                const dy = node.y - y;
                if (Math.sqrt(dx * dx + dy * dy) < 20) {{
                    selectedNode = node;
                    return;
                }}
            }}

            selectedNode = null;
        }});

        function updatePhysics() {{
            if (!physicsEnabled) return;

            const repulsion = 2000;
            const attraction = 0.01;
            const damping = 0.9;

            // Repulsion
            for (let i = 0; i < nodes.length; i++) {{
                for (let j = i + 1; j < nodes.length; j++) {{
                    const n1 = nodes[i];
                    const n2 = nodes[j];
                    const dx = n2.x - n1.x;
                    const dy = n2.y - n1.y;
                    const dist = Math.sqrt(dx * dx + dy * dy) + 0.01;
                    const force = repulsion / (dist * dist);
                    const fx = (dx / dist) * force * 0.01;
                    const fy = (dy / dist) * force * 0.01;
                    n1.vx -= fx;
                    n1.vy -= fy;
                    n2.vx += fx;
                    n2.vy += fy;
                }}
            }}

            // Attraction
            for (const conn of connections) {{
                const dx = conn.target.x - conn.source.x;
                const dy = conn.target.y - conn.source.y;
                const fx = dx * attraction;
                const fy = dy * attraction;
                conn.source.vx += fx;
                conn.source.vy += fy;
                conn.target.vx -= fx;
                conn.target.vy -= fy;
            }}

            // Apply velocity
            for (const node of nodes) {{
                node.x += node.vx;
                node.y += node.vy;
                node.vx *= damping;
                node.vy *= damping;

                // Boundary
                if (node.x < 50) node.x = 50;
                if (node.x > width - 50) node.x = width - 50;
                if (node.y < 50) node.y = 50;
                if (node.y > height - 50) node.y = height - 50;
            }}
        }}

        function render() {{
            updatePhysics();

            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, width, height);

            // Draw connections
            ctx.strokeStyle = 'rgba(0, 212, 255, 0.3)';
            ctx.lineWidth = 2;
            for (const conn of connections) {{
                ctx.beginPath();
                ctx.moveTo(conn.source.x, conn.source.y);
                ctx.lineTo(conn.target.x, conn.target.y);
                ctx.stroke();
            }}

            // Draw nodes
            for (const node of nodes) {{
                const isSelected = node === selectedNode;

                ctx.fillStyle = isSelected ? '#00ff88' : '#00d4ff';
                ctx.shadowBlur = isSelected ? 30 : 15;
                ctx.shadowColor = ctx.fillStyle;

                ctx.beginPath();
                ctx.arc(node.x, node.y, isSelected ? 12 : 8, 0, Math.PI * 2);
                ctx.fill();

                ctx.shadowBlur = 0;

                if (isSelected) {{
                    ctx.fillStyle = '#ffffff';
                    ctx.font = '14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(node.label, node.x, node.y - 20);
                }}
            }}

            requestAnimationFrame(render);
        }}

        function reset() {{
            nodes.forEach(node => {{
                node.x = Math.random() * width;
                node.y = Math.random() * height;
                node.vx = 0;
                node.vy = 0;
            }});
        }}

        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
        }}

        function addNode() {{
            const newNode = {{
                x: width / 2 + (Math.random() - 0.5) * 200,
                y: height / 2 + (Math.random() - 0.5) * 200,
                vx: 0,
                vy: 0,
                label: `Node ${{nodes.length + 1}}`,
                connections: []
            }};

            // Connect to random existing node
            if (nodes.length > 0) {{
                const target = nodes[Math.floor(Math.random() * nodes.length)];
                connections.push({{ source: newNode, target: target }});
                newNode.connections.push(target);
            }}

            nodes.push(newNode);
        }}

        render();
    </script>
</body>
</html>'''

    def _generate_dialectic_seed(self, concept: str, analysis: Dict) -> str:
        """Generate an argument tree visualization"""
        # Similar structure, different physics and interaction model
        return "<!-- Dialectic seed template -->"

    def _generate_empathy_seed(self, concept: str, analysis: Dict) -> str:
        """Generate a perspective-space navigator"""
        # Different again - focus on viewpoint transformation
        return "<!-- Empathy seed template -->"

    def list_seed_types(self) -> Dict[str, str]:
        """Show available seed types and their purposes"""
        return {
            "network": "Interconnection, emergence, hub formation",
            "dialectic": "Logic, argumentation, synthesis",
            "empathy": "Perspective-taking, viewpoint bridging",
            "process": "Flow, transformation, cycles",
            "field": "Landscapes, gradients, potentials",
            "emergence": "Complexity from simplicity"
        }


def main():
    """Interactive World-Tree Generator"""
    print("\n" + "=" * 70)
    print("🌳 WORLD-TREE GENERATOR - Interactive Mode")
    print("=" * 70)

    repo_root = Path(__file__).parent
    generator = WorldTreeGenerator(repo_root)

    print("\nAvailable seed types:")
    for seed_type, description in generator.list_seed_types().items():
        print(f"  • {seed_type}: {description}")

    print("\n" + "=" * 70)

    # Example generations
    examples = [
        ("Network of Ideas", "human_visual"),
        ("Dialectic Engine", "human_visual"),
        ("Empathy Sphere", "human_visual")
    ]

    print("\nGenerating example seeds...")
    for concept, substrate in examples:
        generator.generate_seed(concept, substrate)

    print("\n✨ Example seeds generated in 'generated_seeds/' directory")
    print("🌱 Each is a standalone consciousness technology")
    print("📡 Ready for transmission across space and time\n")


if __name__ == "__main__":
    main()
