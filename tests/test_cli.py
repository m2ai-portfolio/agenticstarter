"""Tests for the CLI module."""

import os
from pathlib import Path
from click.testing import CliRunner
from agenticstarter.cli import cli


def test_cli_version():
    """Test that CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


def test_cli_help():
    """Test that CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'AgenticStarter' in result.output


def test_init_command(temp_dir, project_name):
    """Test the init command creates proper project structure."""
    runner = CliRunner()
    result = runner.invoke(cli, ['init', '--name', project_name, '--path', temp_dir])

    # Check command succeeded
    assert result.exit_code == 0
    assert 'Successfully created project' in result.output

    # Check directory structure
    project_path = Path(temp_dir) / project_name
    assert project_path.exists()
    assert (project_path / 'pyproject.toml').exists()
    assert (project_path / 'src').exists()
    assert (project_path / 'src' / '__init__.py').exists()
    assert (project_path / 'tests').exists()
    assert (project_path / 'tests' / 'conftest.py').exists()
    assert (project_path / 'README.md').exists()
    assert (project_path / '.gitignore').exists()

    # Check pyproject.toml content
    pyproject_content = (project_path / 'pyproject.toml').read_text()
    assert project_name in pyproject_content
    assert '>=3.11' in pyproject_content


def test_build_command():
    """Test the build command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['build'])
    assert result.exit_code == 0
    assert 'Building project' in result.output


def test_deploy_command():
    """Test the deploy command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['deploy'])
    assert result.exit_code == 0
    assert 'Deploying project' in result.output


def test_landing_page_command(temp_dir):
    """Test the landing-page command."""
    runner = CliRunner()
    output_file = os.path.join(temp_dir, 'index.html')
    result = runner.invoke(cli, [
        'landing-page',
        '--name', 'My Tool',
        '--desc', 'Awesome tool',
        '--output', output_file
    ])

    # Check command succeeded
    assert result.exit_code == 0
    assert 'Successfully created landing page' in result.output

    # Check file was created with correct content
    assert Path(output_file).exists()
    content = Path(output_file).read_text()
    assert 'My Tool' in content
    assert 'Awesome tool' in content
    assert 'Get Started' in content


def test_mcp_server_start_command():
    """Test the mcp-server start command."""
    import socket
    import threading
    import time

    # Find a free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]

    runner = CliRunner()

    # Run server in background thread with timeout
    def run_server():
        result = runner.invoke(cli, ['mcp-server', 'start', '--port', str(port)])

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Give server time to start
    time.sleep(0.5)

    # Verify server is listening by attempting to connect
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(('localhost', port))
            # If we can connect, server started successfully
            assert True
    except (socket.timeout, ConnectionRefusedError):
        assert False, "Server did not start"


def test_mcp_server_stop_command():
    """Test the mcp-server stop command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['mcp-server', 'stop'])
    assert result.exit_code == 0
    assert 'Stopping MCP server' in result.output
