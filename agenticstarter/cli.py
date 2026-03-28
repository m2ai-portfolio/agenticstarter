"""Main CLI module for AgenticStarter."""

import click
from agenticstarter.project_template import generate_project


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AgenticStarter - A starter kit for building micro-SaaS agentic tools."""
    pass


@cli.command()
@click.option('--name', default='my-agentic-tool', help='Project name')
@click.option('--path', default='.', help='Target directory path')
def init(name, path):
    """Initialize a new agentic tool project."""
    try:
        generate_project(name, path)
        click.echo(f"✓ Successfully created project '{name}' in {path}/{name}")
        click.echo(f"\nNext steps:")
        click.echo(f"  cd {name}")
        click.echo(f"  python3 -m venv venv")
        click.echo(f"  source venv/bin/activate")
        click.echo(f"  pip install -e .")
    except Exception as e:
        click.echo(f"✗ Error creating project: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--name', required=True, help='Product name')
@click.option('--desc', required=True, help='Product description')
@click.option('--output', default='index.html', help='Output HTML file')
def landing_page(name, desc, output):
    """Generate a landing page for your product."""
    from agenticstarter.landing_page_template import generate_landing_page
    try:
        generate_landing_page(name, desc, output)
        click.echo(f"✓ Successfully created landing page: {output}")
    except Exception as e:
        click.echo(f"✗ Error creating landing page: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('action', type=click.Choice(['start', 'stop']))
@click.option('--port', default=8000, help='Port to run the server on')
@click.option('--host', default='localhost', help='Host to bind the server to')
def mcp_server(action, port, host):
    """Start or stop the MCP server."""
    if action == 'start':
        from agenticstarter.mcp_server import MCPServer
        server = MCPServer(host=host, port=port)
        server.start()
    elif action == 'stop':
        click.echo("Stopping MCP server...")
        click.echo("Note: To stop a running server, use Ctrl+C in the terminal where it's running.")


@cli.command()
def build():
    """Build the project."""
    click.echo("Building project...")
    click.echo("Build functionality coming soon!")


@cli.command()
def deploy():
    """Deploy the project."""
    click.echo("Deploying project...")
    click.echo("Deploy functionality coming soon!")


if __name__ == '__main__':
    cli()
