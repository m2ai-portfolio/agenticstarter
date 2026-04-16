

<p align="center">
  <img src="assets/infographic.png" alt="AgenticStarter: Micro-SaaS Kit for Agentic Tools" width="800">
</p>

<h3 align="center">A starter kit (template + CLI) that generates a micro-SaaS project for an agentic tool, including a landing page (via prompt-to-app), an MCP server for core functionality, extensibility via agentic execution embed, and deployment instructions for solo developers.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
AgenticStarter is a CLI‑driven starter kit that scaffolds a sellable micro‑Saas around an agentic tool. It creates the project structure, a static landing page, and an MCP server so solo developers can go from prototype to product in minutes.

```
$ agenticstarter init my-agentic-tool
Created directory my-agentic-tool with pyproject.toml, src/, and tests/
```

## Problem
Solo developers who build agentic tools struggle with the boilerplate of creating a sellable product (landing page, auth, payments, deployment), causing them to abandon monetization efforts despite having useful tools.

## Features
| Feature | Description |
|---------|-------------|
| Project Scaffold | Generates a complete Python project layout with `pyproject.toml`, source package, and test directory via `agenticstarter init`. |
| Landing Page Generator | Produces a static HTML landing page with product name, description, and call‑to‑action button using `agenticstarter landing-page`. |
| MCP Server | Starts a minimal Model Context Protocol server on `localhost:8000` that handles JSON‑RPC 2.0 messages and supports agentic execution embed via `agenticstarter mcp-server start`. |
| CLI Entrypoint | Provides a unified command line interface with subcommands `init`, `landing-page`, and `mcp-server`. |
| Deployment Instructions | Includes a ready‑to‑use markdown guide for deploying the generated micro‑Saas to common platforms. |

## Quick Start
1. Clone the repository:  
   `git clone https://github.com/m2ai-portfolio/agenticstarter.git`
2. Enter the directory and install the package in editable mode:  
   `cd agenticstarter && pip install -e .`
3. Scaffold a new micro‑Saas project:  
   `agenticstarter init my-agentic-tool`  
   This creates `my-agentic-tool/` with the required files.
4. Generate a landing page for your product:  
   `cd my-agentic-tool && agenticstarter landing-page --name "My Tool" --desc "Awesome tool"`  
   Produces `index.html` containing the heading, description, and a Get Started button.
5. Launch the MCP server to test core functionality:  
   `agenticstarter mcp-server start`  
   The server listens on port 8000 and replies with a `pong` message to a `ping` request.

## Examples
**Initialize a new project**  
```
$ agenticstarter init summary-bot
Created directory summary-bot
 summary-bot/
   pyproject.toml
   src/
   tests/
```
**Create a landing page with custom text**  
```
$ agenticstarter landing-page --name "Summary Bot" --desc "Turn long articles into brief bullets"
```
Resulting `index.html` (excerpt):  
```html
<h1>Summary Bot</h1>
<p>Turn long articles into brief bullets</p>
<a href="#" class="cta-button">Get Started</a>
```
**Run the MCP server and send a ping**  
In one terminal:  
```
$ agenticstarter mcp-server start
MCP server listening on ws://localhost:8000
```
In another terminal (using a simple WS client):  
```
$ wscat -c ws://localhost:8000
> {"jsonrpc":"2.0","method":"ping","id":1}
< {"jsonrpc":"2.0","result":"pong","id":1}
```

## File Structure
```
AgenticStarter: Micro-SaaS Kit for Agentic Tools/
  agenticstarter/          # Core package
    cli.py                 # Click‑based command line interface
    project_template.py    # Scaffold generation logic
    landing_page_template.py # HTML landing page creator
    mcp_server.py          # Minimal MCP server implementation
    deployment_instructions.md # Deployment guide for solo devs
  tests/                   # Unit test suite
    test_project_scaffold.py
    test_landing_page.py
    test_mcp_server.py
  assets/                  # Visual assets
    infographic.png
  screenshots/             # Example outputs and verification screens
  agenticstarter.py        # Console script entry point
  pyproject.toml           # Project metadata and dependencies
  README.md
  LICENSE
  .gitignore
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language runtime |
| click | Building the CLI interface |
| pytest | Running unit tests |

## Contributing
Fork the repo, make your changes, run `pytest` to verify, then submit a pull request.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)