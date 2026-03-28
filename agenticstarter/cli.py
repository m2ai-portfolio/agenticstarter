"""
CLI commands for AgenticStarter
"""

import click
from agenticstarter.project_template import generate_project_scaffold
from agenticstarter.landing_page_template import generate_landing_page
from agenticstarter.mcp_server import MCPServer


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AgenticStarter - A starter kit for creating micro-SaaS products from agentic tools."""
    pass


@cli.command()
@click.option(
    "--name",
    default="my-agentic-tool",
    help="Name of the project to create",
    show_default=True,
)
@click.option(
    "--path",
    default=".",
    help="Path where the project should be created",
    show_default=True,
)
def init(name, path):
    """Generate a project scaffold with standard structure."""
    click.echo(f"Generating project scaffold: {name}")

    try:
        project_path = generate_project_scaffold(name, path)
        click.echo(f"✓ Project scaffold created at: {project_path}")
        click.echo(f"\nNext steps:")
        click.echo(f"  cd {name}")
        click.echo(f"  python -m venv venv")
        click.echo(f"  source venv/bin/activate")
        click.echo(f"  pip install -e .")
    except Exception as e:
        click.echo(f"✗ Error creating project: {e}", err=True)
        raise


@cli.command()
@click.option("--name", required=True, help="Name of the product")
@click.option("--desc", required=True, help="Description of the product")
@click.option(
    "--output",
    default=".",
    help="Directory where index.html should be created",
    show_default=True,
)
def landing_page(name, desc, output):
    """Create a landing page for your micro-SaaS product."""
    click.echo(f"Generating landing page for: {name}")

    try:
        output_file = generate_landing_page(name, desc, output)
        click.echo(f"✓ Landing page created at: {output_file}")
    except Exception as e:
        click.echo(f"✗ Error creating landing page: {e}", err=True)
        raise


@cli.group()
def mcp_server():
    """MCP server commands for Model Context Protocol."""
    pass


@mcp_server.command()
@click.option("--host", default="localhost", help="Host to bind to", show_default=True)
@click.option("--port", default=8000, help="Port to run the server on", show_default=True)
def start(host, port):
    """Start the MCP server."""
    click.echo(f"Starting MCP server on {host}:{port}...")

    try:
        server = MCPServer(host=host, port=port)
        server.start(blocking=True)
    except Exception as e:
        click.echo(f"✗ Error starting MCP server: {e}", err=True)
        raise


@cli.command()
def build():
    """Build the project (placeholder)."""
    click.echo("Build command - placeholder for future implementation")


@cli.command()
def deploy():
    """Deploy the project (placeholder)."""
    click.echo("Deploy command - placeholder for future implementation")


if __name__ == "__main__":
    cli()
