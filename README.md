# AgenticStarter

A CLI starter kit for generating micro-SaaS projects for agentic tools.

## Overview

AgenticStarter provides a template and CLI to quickly productize agentic tools. It includes:
- **Project Scaffold Generator** - Creates a ready-to-use micro-SaaS project structure
- **Landing Page Generator** - Creates static HTML landing pages via prompt-to-app
- **MCP Server** - Minimal Model Context Protocol server for core agentic functionality

## Tech Stack
- Python 3.11+
- click (CLI framework)
- pytest (testing)

## Getting Started

```bash
# Install dependencies
pip install -e .

# Initialize a new project
agenticstarter init

# Generate a landing page
agenticstarter landing-page --name "My Tool" --desc "Awesome tool"

# Start MCP server
agenticstarter mcp-server start
```

## Development

```bash
# Run the dev setup
bash init.sh

# Run tests
pytest
```
