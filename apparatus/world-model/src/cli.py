"""
World Model CLI: Command-line interface for the knowledge system
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


@click.group()
@click.pass_context
def cli(ctx):
    """World Model - Local Consciousness Knowledge System"""
    ctx.ensure_object(dict)


@cli.command()
@click.option('--force', '-f', is_flag=True, help='Re-ingest even if already processed')
@click.pass_context
def ingest(ctx, force):
    """Ingest all esoterica content into the world model"""
    from .world import WorldModel

    console.print("[bold blue]Initializing World Model...[/bold blue]")
    world = WorldModel()

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
@click.pass_context
def search(ctx, query, limit):
    """Search the world model"""
    from .world import WorldModel

    world = WorldModel()
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
@click.pass_context
def explore(ctx, entity, depth):
    """Explore connections for an entity"""
    from .world import WorldModel

    world = WorldModel()
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

    # Display edges
    console.print(f"\n[bold]Relations:[/bold]")
    for edge in result.get("edges", []):
        console.print(f"  {edge['source']} --[{edge.get('type', 'relates')}]--> {edge['target']}")


@cli.command()
@click.argument('source')
@click.argument('target')
@click.pass_context
def path(ctx, source, target):
    """Find path between two entities"""
    from .world import WorldModel

    world = WorldModel()
    world.load()

    console.print(f"[bold blue]Finding path:[/bold blue] {source} → {target}\n")

    result = world.find_path(source, target)

    if not result:
        console.print("[yellow]No path found[/yellow]")
        return

    console.print("[bold green]Path found:[/bold green]")
    console.print(" → ".join(result))


@cli.command()
@click.argument('query')
@click.option('--chunks', '-k', default=5, help='Number of context chunks')
@click.pass_context
def context(ctx, query, chunks):
    """Get LLM context for a query"""
    from .world import WorldModel

    world = WorldModel()
    world.load()

    context_str = world.get_context(query, k=chunks)

    console.print(Panel(
        Markdown(context_str),
        title="Context for LLM",
        border_style="blue"
    ))


@cli.command()
@click.pass_context
def stats(ctx):
    """Show world model statistics"""
    from .world import WorldModel

    world = WorldModel()
    world.load()

    stats = world.stats()

    table = Table(title="World Model Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Entities", str(stats.get("entities", 0)))
    table.add_row("Relations", str(stats.get("relations", 0)))
    table.add_row("Documents", str(stats.get("documents", 0)))
    table.add_row("Chunks", str(stats.get("chunks", 0)))
    table.add_row("Last Updated", stats.get("last_updated", "unknown"))

    console.print(table)


@cli.command()
@click.option('--port', '-p', default=8000, help='Server port')
@click.pass_context
def serve(ctx, port):
    """Start the API server"""
    console.print(f"[bold blue]Starting server on port {port}...[/bold blue]")
    console.print("[yellow]API server not yet implemented[/yellow]")
    # TODO: Implement FastAPI server


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
