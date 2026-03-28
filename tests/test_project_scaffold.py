"""
Tests for project scaffold generation
"""

import pytest
from pathlib import Path
from agenticstarter.project_template import generate_project_scaffold


def test_generate_project_scaffold_creates_directory(tmp_path):
    """Test that generate_project_scaffold creates the project directory."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    assert project_path.exists()
    assert project_path.is_dir()
    assert project_path.name == project_name


def test_generate_project_scaffold_creates_pyproject_toml(tmp_path):
    """Test that generate_project_scaffold creates pyproject.toml."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    pyproject_file = project_path / "pyproject.toml"
    assert pyproject_file.exists()
    assert pyproject_file.is_file()

    content = pyproject_file.read_text()
    assert "name = \"test-project\"" in content
    assert "version = \"0.1.0\"" in content
    assert "requires-python = \">=3.11\"" in content


def test_generate_project_scaffold_creates_src_directory(tmp_path):
    """Test that generate_project_scaffold creates src/ package directory."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    src_dir = project_path / "src" / "test_project"
    assert src_dir.exists()
    assert src_dir.is_dir()

    init_file = src_dir / "__init__.py"
    assert init_file.exists()
    assert init_file.is_file()


def test_generate_project_scaffold_creates_tests_directory(tmp_path):
    """Test that generate_project_scaffold creates tests/ directory."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    tests_dir = project_path / "tests"
    assert tests_dir.exists()
    assert tests_dir.is_dir()

    init_file = tests_dir / "__init__.py"
    assert init_file.exists()
    assert init_file.is_file()


def test_generate_project_scaffold_creates_readme(tmp_path):
    """Test that generate_project_scaffold creates README.md."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    readme_file = project_path / "README.md"
    assert readme_file.exists()
    assert readme_file.is_file()

    content = readme_file.read_text()
    assert "test-project" in content


def test_generate_project_scaffold_creates_gitignore(tmp_path):
    """Test that generate_project_scaffold creates .gitignore."""
    project_name = "test-project"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    gitignore_file = project_path / ".gitignore"
    assert gitignore_file.exists()
    assert gitignore_file.is_file()

    content = gitignore_file.read_text()
    assert "__pycache__/" in content
    assert "venv/" in content


def test_generate_project_scaffold_raises_on_existing_directory(tmp_path):
    """Test that generate_project_scaffold raises error if directory exists."""
    project_name = "test-project"

    # Create the project once
    generate_project_scaffold(project_name, str(tmp_path))

    # Try to create it again - should raise FileExistsError
    with pytest.raises(FileExistsError):
        generate_project_scaffold(project_name, str(tmp_path))


def test_generate_project_scaffold_handles_project_name_with_hyphens(tmp_path):
    """Test that project names with hyphens are converted to underscores for package names."""
    project_name = "my-agentic-tool"
    project_path = generate_project_scaffold(project_name, str(tmp_path))

    # Directory name should keep hyphens
    assert project_path.name == "my-agentic-tool"

    # But package name should use underscores
    src_dir = project_path / "src" / "my_agentic_tool"
    assert src_dir.exists()
    assert src_dir.is_dir()
