#!/bin/bash
# AgenticStarter - Development Setup & Run Script

set -e

echo "Setting up AgenticStarter development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install click pytest --quiet

# Install the package in development mode
pip install -e . --quiet 2>/dev/null || echo "Package not yet installable (pyproject.toml may not exist yet)"

echo ""
echo "AgenticStarter development environment ready!"
echo "Virtual environment activated at ./venv"
echo ""
echo "Available commands:"
echo "  python agenticstarter.py init              - Generate project scaffold"
echo "  python agenticstarter.py landing-page      - Create landing page"
echo "  python agenticstarter.py mcp-server start  - Start MCP server"
echo "  pytest                                     - Run tests"
