"""Tests for the project_template module."""

from pathlib import Path
from agenticstarter.project_template import generate_project


def test_generate_project(temp_dir, project_name):
    """Test that generate_project creates the correct structure."""
    project_path = generate_project(project_name, temp_dir)

    # Verify project directory exists
    assert Path(project_path).exists()

    # Verify src directory and files
    src_dir = Path(project_path) / 'src'
    assert src_dir.exists()
    assert (src_dir / '__init__.py').exists()

    # Verify tests directory and files
    tests_dir = Path(project_path) / 'tests'
    assert tests_dir.exists()
    assert (tests_dir / '__init__.py').exists()
    assert (tests_dir / 'conftest.py').exists()

    # Verify pyproject.toml
    pyproject = Path(project_path) / 'pyproject.toml'
    assert pyproject.exists()
    content = pyproject.read_text()
    assert project_name in content
    assert 'requires-python = ">=3.11"' in content
    assert 'pytest' in content

    # Verify README.md
    readme = Path(project_path) / 'README.md'
    assert readme.exists()
    assert project_name in readme.read_text()

    # Verify .gitignore
    gitignore = Path(project_path) / '.gitignore'
    assert gitignore.exists()
    assert '__pycache__' in gitignore.read_text()


def test_generate_project_default_name(temp_dir):
    """Test generate_project with default project name."""
    project_path = generate_project('my-agentic-tool', temp_dir)
    assert Path(project_path).exists()
    assert 'my-agentic-tool' in project_path
