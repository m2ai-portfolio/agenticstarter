
<p align="center">
  <img src="assets/infographic.png" alt="Agenticstarter" width="800">
</p>

<h3 align="center">ONE-LINE DESCRIPTION OF WHAT THIS DOES</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

Agenticstarter is a starter kit that provides a template and CLI to generate a micro-SaaS project for an agentic tool.
$ agenticstarter init
[Creates a folder `my-agentic-tool` containing `pyproject.toml`, `src/`, and `tests/` directories.]

| Feature | Description |
|---------|-------------|
| Project Scaffold | Generates a ready-to-use micro-SaaS project structure with standard files and CLI entry point. |
| Landing Page Generator | Creates a static HTML landing page for the micro-SaaS product using a prompt-to-app mechanism. |
| MCP Server | Provides a minimal Model Context Protocol server for core agentic functionality, with extensibility via agentic execution embed. |

1. Clone the repository: `git clone https://github.com/m2ai-portfolio/agenticstarter.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the CLI: `agenticstarter init`

**Basic Initialization**
$ agenticstarter init
[Creates a folder `my-agentic-tool` containing `pyproject.toml`, `src/`, and `tests/` directories.]

**Generate Landing Page**
$ agenticstarter landing-page --name "My Tool" --desc "Awesome tool"
[Produces `index.html` containing a heading "My Tool", a paragraph "Awesome tool", and a button "Get Started".]

**Start MCP Server**
$ agenticstarter mcp-server start
[Listens on port 8000 and responds with a `pong` message to a `ping` request.]

Agenticstarter/
  src/          # Core source code
    agenticstarter.py          # Main CLI
    agenticstarter/project_template.py  # Project template
    agenticstarter/landing_page_template.py  # Landing page template
    agenticstarter/mcp_server.py  # MCP server
    agenticstarter/deployment_instructions.md  # Deployment instructions
  tests/        # Test suite
    test_project_scaffold.py  # Test for project scaffold

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language |
| click | CLI framework |
| pytest | Testing framework |

Brief section: fork, edit, test, PR.

MIT

Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)