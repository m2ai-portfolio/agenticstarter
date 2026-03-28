"""Pytest configuration and fixtures for AgenticStarter tests."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup after test
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def project_name():
    """Provide a default project name for tests."""
    return "test-project"
