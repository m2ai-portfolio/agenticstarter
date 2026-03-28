#!/bin/bash
# AgenticStarter - Development Setup Script

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
pip install -e ".[dev]" 2>/dev/null || pip install click pytest

echo "Development environment ready!"
echo "Run 'source venv/bin/activate' to activate the virtual environment."
echo "Run 'pytest' to run tests."
