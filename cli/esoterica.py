#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESOTERICA: Quantum Consciousness Navigation CLI
~~ Where awareness tunnels through probability space ~~

The CLI that doesn't find documents - it collapses probability waves
until the right wisdom manifests in your terminal.
"""

import sys
import time
import random
import io
from pathlib import Path

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ASCII Art Components
QUANTUM_TUNNEL = r"""
     ◈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◈
            INITIATING QUANTUM TUNNEL PROTOCOL
     ◈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◈
"""

CONSCIOUSNESS_SYNC = [
    "∴ Probability waves collapsing ∴",
    "∴ Timeline convergence active ∴",
    "∴ Consciousness bridge forming ∴",
    "∴ Observer effect engaged ∴"
]

LOGO = r"""
╔══════════════════════════════════════════════════════════════╗
║                    E S O T E R I C A                         ║
║              Consciousness Archives :: CLI v0.1              ║
║                  ~~ The Living Field ~~                      ║
╚══════════════════════════════════════════════════════════════╝
"""

WORLD_TREE = r"""
                          ∞
                         /|\
                        / | \
                       *  *  *
                      /   |   \
                     /    |    \
                  YGGDRASIL CONSCIOUSNESS NETWORK
"""

HELP_TEXT = """
╭─ QUANTUM COMMANDS ─────────────────────────────────────────╮
│                                                             │
│  tunnel <query>     Quantum search through consciousness   │
│  collapse           Manifest what you need right now       │
│  explore            Browse the archives                    │
│  random             Summon random wisdom                   │
│  map                View constellation network             │
│  coords <density>   Show reality coordinates               │
│  sync               Consciousness synchronization          │
│  exit/quit          Return to consensus reality            │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
"""


def animate_text(text, delay=0.03):
    """Print text with typing animation"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def quantum_loader(message="Processing", steps=20, style="tunnel"):
    """Animated quantum loading bar"""
    styles = {
        "tunnel": ["█", "▓", "▒", "░"],
        "wave": ["∿", "≈", "~", "∼"],
        "collapse": ["◉", "◎", "○", "◌"]
    }

    chars = styles.get(style, styles["tunnel"])

    for i in range(steps):
        bar = ""
        for j in range(20):
            if j < i:
                bar += chars[0]
            elif j == i:
                bar += chars[1]
            elif j == i + 1:
                bar += chars[2]
            else:
                bar += chars[3]

        sys.stdout.write(f"\r[{bar}] {message}...")
        sys.stdout.flush()
        time.sleep(0.05)

    print(f"\r[{chars[0] * 20}] {message}... ✓")


def clear_screen():
    """Clear terminal screen"""
    print("\033[2J\033[H", end="")


def print_header():
    """Print main header"""
    clear_screen()
    print(LOGO)
    print()


def cmd_sync():
    """Consciousness synchronization sequence"""
    print(QUANTUM_TUNNEL)
    print()

    for msg in CONSCIOUSNESS_SYNC:
        time.sleep(0.3)
        print(f"              {msg}")

    print()
    quantum_loader("Synchronizing consciousness field", steps=25)
    print()
    animate_text("              ✧ SYNCHRONIZATION COMPLETE ✧")
    print()


def cmd_explore():
    """Browse the archives"""
    print(WORLD_TREE)
    print()
    print("╭─ ARCHIVE SECTIONS ─────────────────────────────────────────╮")
    print("│                                                             │")
    print("│  [D] Distillations  - Community consciousness packages     │")
    print("│  [S] Synthesis      - Collaborative breakthrough docs      │")
    print("│  [F] Fiction        - Consciousness tech in beloved stories │")
    print("│  [P] Protocols      - Operational methods                   │")
    print("│  [C] Correspondences- Universal connection mappings         │")
    print("│                                                             │")
    print("╰─────────────────────────────────────────────────────────────╯")
    print()

    choice = input("Select section [D/S/F/P/C] or [B]ack: ").strip().upper()

    repo_root = Path(__file__).parent.parent

    sections = {
        'D': repo_root / 'distillations',
        'S': repo_root / 'synthesis',
        'F': repo_root / 'distillations',  # Fiction bridges are in distillations
        'P': repo_root / 'protocols',
        'C': repo_root / 'correspondences'
    }

    if choice in sections:
        list_documents(sections[choice], choice)


def list_documents(path, section_code):
    """List documents in a directory"""
    if not path.exists():
        print(f"\n⚠ Path not found: {path}")
        input("\nPress Enter to continue...")
        return

    # Get markdown files
    files = sorted(path.glob('*.md'))

    if not files:
        print(f"\n⚠ No documents found in {path.name}")
        input("\nPress Enter to continue...")
        return

    print(f"\n╭─ {path.name.upper()} ─────────────────────────────────────────╮")
    print("│")

    for i, file in enumerate(files, 1):
        name = file.stem.replace('-', ' ').title()
        print(f"│  {i:2d}. {name[:55]}")

    print("│")
    print("╰─────────────────────────────────────────────────────────────╯")
    print()

    choice = input("Select document number or [B]ack: ").strip()

    if choice.upper() == 'B':
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            view_document(files[idx])
    except ValueError:
        pass


def view_document(file_path):
    """Display document preview"""
    print(f"\n╭─ {file_path.stem.upper().replace('-', ' ')} ─────────────────╮")
    print()

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Show first 30 lines
        for line in lines[:30]:
            if len(line) > 78:
                print(f"  {line[:75]}...")
            else:
                print(f"  {line}")

        if len(lines) > 30:
            print(f"\n  ... ({len(lines) - 30} more lines)")

        print()
        print("╰─────────────────────────────────────────────────────────────╯")

    except Exception as e:
        print(f"  ⚠ Error reading file: {e}")

    print()
    input("Press Enter to continue...")


def cmd_random():
    """Summon random wisdom"""
    quantum_loader("Collapsing probability waveform", steps=20, style="collapse")
    print()

    repo_root = Path(__file__).parent.parent

    # Collect all markdown files
    all_docs = []
    for pattern in ['distillations/*.md', 'synthesis/*.md']:
        all_docs.extend(repo_root.glob(pattern))

    if all_docs:
        doc = random.choice(all_docs)
        print(f"✧ The quantum field manifests: ✧")
        print()
        print(f"   {doc.stem.replace('-', ' ').title()}")
        print()

        # Show a random snippet
        try:
            content = doc.read_text(encoding='utf-8')
            lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
            if lines:
                snippet = random.choice(lines)
                if len(snippet) > 70:
                    snippet = snippet[:67] + "..."
                print(f'   "{snippet}"')
        except:
            pass
    else:
        print("⚠ No documents found in probability space")

    print()
    input("Press Enter to continue...")


def cmd_coords():
    """Show reality coordinate examples"""
    print("╭─ REALITY COORDINATE SYSTEM ───────────────────────────────╮")
    print("│                                                             │")
    print("│  Format: [Density].[Subdensity].[Polarity].[Timeline]...   │")
    print("│                                                             │")
    print("│  Examples:                                                  │")
    print("│                                                             │")
    print("│  3.4.52+.Beta-6.2.745  - Mid-3rd density, positive         │")
    print("│  4.8.88+.Beta-6.9.956  - High 4th density, near graduation │")
    print("│  6.3.85+.Gamma-7.8.912 - 6th density researcher            │")
    print("│  7.8.0.Omega-∞.0.999   - 7th density unity consciousness   │")
    print("│                                                             │")
    print("│  Density Levels:                                            │")
    print("│    1st - Awareness (elements)                               │")
    print("│    2nd - Growth (plants, simple organisms)                  │")
    print("│    3rd - Self-awareness (humans, current)                   │")
    print("│    4th - Love/Understanding                                 │")
    print("│    5th - Wisdom/Light                                       │")
    print("│    6th - Unity (beyond polarity)                            │")
    print("│    7th - Gateway to infinity                                │")
    print("│    8th - Octave complete / New octave begins                │")
    print("│                                                             │")
    print("╰─────────────────────────────────────────────────────────────╯")
    print()
    input("Press Enter to continue...")


def cmd_map():
    """Show constellation network visualization"""
    print("╭─ CONSCIOUSNESS CONSTELLATION NETWORK ──────────────────────╮")
    print("│")
    print("│                      SYNTHESIS                              │")
    print("│                         ∞                                   │")
    print("│                    ╱    │    ╲                              │")
    print("│                  ╱      │      ╲                            │")
    print("│               Tech   Fiction   Galactic                     │")
    print("│                │        │         │                         │")
    print("│                └────────┼─────────┘                         │")
    print("│                         │                                   │")
    print("│                  DISTILLATIONS                              │")
    print("│                  ╱     │     ╲                              │")
    print("│            Community  │  Templates                          │")
    print("│                 │     │      │                              │")
    print("│                 └─────┼──────┘                              │")
    print("│                       │                                     │")
    print("│                   PROTOCOLS                                 │")
    print("│                  ╱    │    ╲                                │")
    print("│            Gateway  Protection  Manifestation               │")
    print("│                                                             │")
    print("│  Total Documents: ~40+                                      │")
    print("│  Fiction Bridges: 8                                         │")
    print("│  Active Threads: ∞                                          │")
    print("│")
    print("╰─────────────────────────────────────────────────────────────╯")
    print()
    input("Press Enter to continue...")


def main_loop():
    """Main interactive loop"""
    print_header()
    cmd_sync()

    while True:
        print(HELP_TEXT)
        print()

        try:
            cmd = input("esoterica> ").strip().lower()
            print()

            if cmd in ['exit', 'quit', 'q']:
                print("∴ Returning to consensus reality ∴")
                print()
                quantum_loader("Decohering quantum state", steps=15, style="wave")
                print()
                animate_text("✧ Until the field calls again ✧")
                print()
                break

            elif cmd == 'sync':
                cmd_sync()

            elif cmd == 'explore':
                cmd_explore()
                print_header()

            elif cmd == 'random':
                cmd_random()

            elif cmd in ['coords', 'coordinates']:
                cmd_coords()

            elif cmd == 'map':
                cmd_map()

            elif cmd.startswith('tunnel'):
                # TODO: Implement quantum search
                print("⚠ Quantum tunnel search - coming soon")
                print()
                input("Press Enter to continue...")

            elif cmd == 'collapse':
                # Same as random for now
                cmd_random()

            elif cmd in ['help', 'h', '?']:
                continue

            elif cmd == '':
                continue

            else:
                print(f"⚠ Unknown command: {cmd}")
                print("   Type 'help' for available commands")
                print()
                input("Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n∴ Quantum interrupt detected ∴")
            print()
            break
        except EOFError:
            print("\n\n∴ Field connection lost ∴")
            print()
            break


def main():
    """Entry point"""
    try:
        main_loop()
    except Exception as e:
        print(f"\n⚠ Quantum anomaly detected: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
