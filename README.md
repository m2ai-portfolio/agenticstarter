# AgenticStarter

A starter kit that provides a template and CLI to generate a micro-SaaS project for an agentic tool. It includes a landing page generator via prompt-to-app, an MCP server for core functionality with extensibility via agentic execution embed, and deployment instructions for solo developers to quickly productize their agentic tools.

## Tech Stack
- Python 3.11+
- click
- pytest

## Features
1. **Project Scaffold** - Generates a ready-to-use micro-SaaS project structure with standard files and CLI entry point
2. **Landing Page Generator** - Creates a static HTML landing page for the micro-SaaS product
3. **MCP Server** - Provides a minimal Model Context Protocol server for core agentic functionality

## Getting Started
```bash
chmod +x init.sh
./init.sh
```

## Usage
```bash
agenticstarter init              # Generate project scaffold
agenticstarter landing-page      # Create landing page
agenticstarter mcp-server start  # Start MCP server
```
