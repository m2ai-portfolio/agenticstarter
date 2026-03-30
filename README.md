

# AgenticStarter: Micro-SaaS Kit for Agentic Tools

## Overview
The AgenticStarter is a starter kit that provides a template and CLI to generate a micro-SaaS project for an agentic tool. It includes a landing page generator via prompt-to-app, an MCP server for core functionality with extensibility via agentic execution embed, and deployment instructions for solo developers to quickly productize their agentic tools.

## Problem Statement
Solo developers who build agentic tools struggle with the boilerplate of creating a sellable product (landing page, auth, payments, deployment), causing them to abandon monetization efforts despite having useful tools.

## Features
- Generates a ready-to-use micro-SaaS project structure with standard files and CLI entry point
- Creates a static HTML landing page for the micro-SaaS product using a prompt-to-app mechanism
- Provides a minimal Model Context Protocol server for core agentic functionality, with extensibility via agentic execution embed

## Tech Stack
- Python 3.11+
- click
- pytest

## Quick Start / Installation
To get started locally:
1. Install Python 3.11+
2. Install required dependencies (click, pytest) via pip
3. Run the CLI: `agenticstarter` (assuming it's installed and in PATH)

## Usage
Example usage:
- To initialize a new project: `agenticstarter init --name "my-agentic-tool"`
- To generate a landing page: `agenticstarter landing-page --name "My Tool" --desc "Awesome tool"`
- To start the MCP server: `agenticstarter mcp-server start`

## Architecture
The code is organized as follows:
- `agenticstarter.py`: Main CLI entry point
- `agenticstarter/project_template.py`: Project scaffold template
- `agenticstarter/landing_page_template.py`: Landing page generator template
- `agenticstarter/mcp_server.py`: MCP server template
- `agenticstarter/deployment_instructions.md`: Deployment instructions

## License
MIT