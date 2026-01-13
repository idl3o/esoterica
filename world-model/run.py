#!/usr/bin/env python3
"""
Quick start script for World Model

Usage:
    python run.py ingest      # Ingest all content
    python run.py search "query"   # Search
    python run.py stats       # Show stats
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Now we can do direct imports
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console(force_terminal=True, legacy_windows=False)


def get_world_model():
    """Lazy import and instantiate WorldModel"""
    from world import WorldModel
    return WorldModel()


@click.group()
def cli():
    """World Model - Local Consciousness Knowledge System"""
    pass


@cli.command()
@click.option('--force', '-f', is_flag=True, help='Re-ingest even if already processed')
def ingest(force):
    """Ingest all esoterica content into the world model"""
    console.print("[bold blue]Initializing World Model...[/bold blue]")
    world = get_world_model()

    console.print("[bold blue]Starting ingestion...[/bold blue]")
    with console.status("[bold green]Processing documents..."):
        stats = world.ingest_all(force=force)

    # Display results
    table = Table(title="Ingestion Complete")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")

    table.add_row("Documents", str(stats.get("documents", 0)))
    table.add_row("Entities", str(stats.get("entities", 0)))
    table.add_row("Relations", str(stats.get("relations", 0)))
    table.add_row("Chunks", str(stats.get("chunks", 0)))

    console.print(table)


@cli.command()
@click.argument('query')
@click.option('--limit', '-k', default=10, help='Number of results')
def search(query, limit):
    """Search the world model"""
    world = get_world_model()
    world.load()

    console.print(f"[bold blue]Searching:[/bold blue] {query}\n")

    with console.status("[bold green]Searching..."):
        results = world.search(query, k=limit)

    if not results:
        console.print("[yellow]No results found[/yellow]")
        return

    for i, result in enumerate(results, 1):
        score = result.get("combined_score", 0)
        source = result.get("source", result.get("id", "unknown"))
        content = result.get("content", "")[:200]

        panel = Panel(
            f"{content}...",
            title=f"[{i}] {source}",
            subtitle=f"Score: {score:.3f}",
            border_style="green" if score > 0.5 else "yellow"
        )
        console.print(panel)
        console.print()


@cli.command()
@click.argument('entity')
@click.option('--depth', '-d', default=1, help='Depth of connections to show')
def explore(entity, depth):
    """Explore connections for an entity"""
    world = get_world_model()
    world.load()

    console.print(f"[bold blue]Exploring:[/bold blue] {entity}\n")

    result = world.get_connections(entity, depth=depth)

    if not result.get("nodes"):
        console.print(f"[yellow]Entity '{entity}' not found[/yellow]")
        return

    # Display center entity
    center = result.get("center")
    console.print(f"[bold green]Center:[/bold green] {center}\n")

    # Display connected nodes
    table = Table(title=f"Connections (depth={depth})")
    table.add_column("Entity", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Description", style="white")

    for node in result.get("nodes", []):
        if node["id"] != center:
            table.add_row(
                node.get("name", node["id"]),
                node.get("type", "unknown"),
                node.get("description", "")[:50]
            )

    console.print(table)


@cli.command()
def stats():
    """Show world model statistics"""
    world = get_world_model()
    world.load()

    s = world.stats()

    table = Table(title="World Model Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Entities", str(s.get("entities", 0)))
    table.add_row("Relations", str(s.get("relations", 0)))
    table.add_row("Documents", str(s.get("documents", 0)))
    table.add_row("Chunks", str(s.get("chunks", 0)))
    table.add_row("Last Updated", s.get("last_updated", "unknown"))

    console.print(table)


if __name__ == "__main__":
    cli()
