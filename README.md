

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
AgenticStarter is a starter kit that lets solo developers spin up a sellable micro‑SaaS around an agentic tool in minutes. It provides a CLI that scaffolds a project, creates a landing page from a simple prompt, and launches an MCP server for the core agentic logic.

```
$ agenticstarter init my-agentic-tool
Created directory my-agentic-tool
Initialized pyproject.toml
Created src/ and tests/ folders
```

## Problem
Solo developers who build agentic tools struggle with the boilerplate of creating a sellable product -- landing page, auth, payments, deployment -- causing them to abandon monetization efforts despite having useful tools.

## Features
| Feature | Description |
|---------|-------------|
| Project Scaffold | Generates a ready‑to‑use Python package with `pyproject.toml`, `src/`, and `tests/` via `agenticstarter init`. |
| Landing Page Creator | Produces a static HTML landing page with meta tags and a CTA button from product name and description. |
| MCP Server | Implements a minimal Model Context Protocol server that handles JSON‑RPC 2.0 messages and supports agentic execution embed. |
| CLI Entry Point | Provides a single `agenticstarter` command with subcommands `init`, `landing-page`, and `mcp-server`. |
| Deployment Instructions | Includes a markdown guide for deploying the generated micro‑SaaS to common platforms. |

## Quick Start
1. Clone the repository:  
   ```bash
   git clone https://github.com/m2ai-portfolio/agenticstarter.git
   cd agenticstarter
   ```
2. Install the package in editable mode:  
   ```bash
   pip install -e .
   ```
3. Scaffold a new micro‑SaaS project:  
   ```bash
   agenticstarter init my-agentic-tool
   ```
4. Change into the new project and install its dependencies:  
   ```bash
   cd my-agentic-tool
   pip install -e .
   ```
5. Generate a landing page for your tool:  
   ```bash
   agenticstarter landing-page --name "Text Summarizer" --desc "Condenses long articles into short summaries"
   ```
6. Start the MCP server to test core functionality:  
   ```bash
   agenticstarter mcp-server start
   ```

## Examples
**Initialize a new micro‑SaaS project**  
```
$ agenticstarter init my-fancy-tool
Created directory my-fancy-tool
Initialized pyproject.toml
Created src/my_fancy_tool/ and tests/ folders
```
*Output shows the new project scaffold with standard files.*

**Generate a landing page**  
```
$ agenticstarter landing-page --name "Code Review Bot" --desc "AI‑powered bot that suggests improvements on pull requests"
Created index.html
```
*Output confirms the HTML file was written; opening it reveals a heading “Code Review Bot”, a description paragraph, and a “Get Started” button.*

**Start the MCP server and test a ping**  
```
$ agenticstarter mcp-server start
MCP server listening on localhost:8000
```
*In another terminal:*  
```
$ curl -s -X POST http://localhost:8000 -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"ping","id":1}'
{"jsonrpc":"2.0","result":"pong","id":1}
```
*The server responds with a pong message, confirming the MCP endpoint is operational.*

## File Structure
```
AgenticStarter: Micro-SaaS Kit for Agentic Tools/
  src/agenticstarter/          # Core source code
    cli.py                     # CLI entry point (init, landing-page, mcp-server)
    project_template.py        # Project scaffolding logic
    landing_page_template.py   # HTML landing page generator
    mcp_server.py              # MCP server implementation
  tests/                       # Test suite
    test_cli.py
    test_landing_page.py
    test_mcp_server.py
    test_project_template.py
  assets/                      # Static assets
    infographic.png
  pyproject.toml               # Project configuration and dependencies
  README.md                    # This file
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language runtime |
| click | Building the CLI interface |
| pytest | Running the test suite |

## Contributing
Fork the repo, make changes, run `pytest` to verify, then submit a pull request.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)