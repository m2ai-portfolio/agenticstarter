"""Project template generator for AgenticStarter."""

import os
from pathlib import Path


def generate_project(name, target_path='.'):
    """
    Generate a new agentic tool project with standard structure.

    Args:
        name: Project name
        target_path: Directory where the project should be created
    """
    # Create project directory
    project_dir = Path(target_path) / name
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create src directory with __init__.py
    src_dir = project_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    (src_dir / '__init__.py').write_text('"""Main package for the agentic tool."""\n\n__version__ = "0.1.0"\n')

    # Create tests directory with conftest.py
    tests_dir = project_dir / 'tests'
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / '__init__.py').write_text('"""Tests package."""\n')
    (tests_dir / 'conftest.py').write_text('''"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"test": "data"}
''')

    # Create pyproject.toml
    pyproject_content = f'''[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = "An agentic tool built with AgenticStarter"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
'''
    (project_dir / 'pyproject.toml').write_text(pyproject_content)

    # Create README.md
    readme_content = f'''# {name}

An agentic tool built with AgenticStarter.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
'''
    (project_dir / 'README.md').write_text(readme_content)

    # Create .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Build
dist/
build/
*.egg-info/
'''
    (project_dir / '.gitignore').write_text(gitignore_content)

    return str(project_dir)
