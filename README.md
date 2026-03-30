# AgenticStarter

A CLI starter kit that scaffolds micro-SaaS projects for agentic tools. Generates project structure, a static landing page, and a Model Context Protocol (MCP) server — so you ship the product instead of writing boilerplate.

## Install

```bash
git clone https://github.com/m2ai-portfolio/agenticstarter.git
cd agenticstarter
pip install -e .
```

Requires Python 3.11+.

## Usage

### Scaffold a new project

```bash
agenticstarter init --name "my-agent" --path ./projects
```

Creates a standard layout: `pyproject.toml`, `src/`, `tests/`, and a CLI entry point.

### Generate a landing page

```bash
agenticstarter landing-page --name "My Agent" --desc "Automates X for Y" --output ./site
```

Outputs a self-contained `index.html` with meta tags, responsive layout, and a call-to-action button. Input is sanitized against XSS.

### Start the MCP server

```bash
agenticstarter mcp-server start --host localhost --port 8000
```

Launches a JSON-RPC 2.0 server that supports tool registration for agentic execution:

```python
from agenticstarter.mcp_server import MCPServer

server = MCPServer(host="localhost", port=8000)
server.register_tool("summarize", my_summarize_handler)
server.start(blocking=True)
```

## Project Structure

```
agenticstarter/
  cli.py                    # Click CLI (init, landing-page, mcp-server)
  project_template.py       # Project scaffold generator
  landing_page_template.py  # HTML landing page generator
  mcp_server.py             # JSON-RPC 2.0 MCP server
  deployment_instructions.md
tests/
  test_project_scaffold.py
  test_landing_page.py
  test_mcp_server.py
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT
