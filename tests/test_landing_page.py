"""
Tests for landing page generation
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from agenticstarter.landing_page_template import generate_landing_page
from agenticstarter.cli import cli


def test_generate_landing_page_creates_index_html(tmp_path):
    """Test that generate_landing_page creates index.html file."""
    name = "Test Product"
    description = "This is a test product"

    output_file = generate_landing_page(name, description, str(tmp_path))

    assert output_file.exists()
    assert output_file.is_file()
    assert output_file.name == "index.html"


def test_generate_landing_page_contains_product_name_in_h1(tmp_path):
    """Test that the generated HTML contains the product name in an h1 tag."""
    name = "My Amazing Tool"
    description = "A great tool for developers"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    assert "<h1>My Amazing Tool</h1>" in content


def test_generate_landing_page_contains_description_in_p(tmp_path):
    """Test that the generated HTML contains the description in a p tag."""
    name = "My Tool"
    description = "Awesome tool for testing"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    assert "<p>Awesome tool for testing</p>" in content


def test_generate_landing_page_contains_get_started_button(tmp_path):
    """Test that the generated HTML contains a 'Get Started' button."""
    name = "Test"
    description = "Test description"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    assert "<button>Get Started</button>" in content


def test_generate_landing_page_has_proper_meta_tags(tmp_path):
    """Test that the generated HTML has proper meta tags."""
    name = "Product Name"
    description = "Product description"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    # Check for DOCTYPE
    assert "<!DOCTYPE html>" in content

    # Check for meta charset
    assert '<meta charset="UTF-8">' in content

    # Check for meta viewport
    assert '<meta name="viewport"' in content

    # Check for meta description
    assert '<meta name="description" content="Product description">' in content


def test_generate_landing_page_has_proper_html_structure(tmp_path):
    """Test that the generated HTML has proper HTML5 structure."""
    name = "Test"
    description = "Test"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    # Check for proper HTML structure
    assert "<!DOCTYPE html>" in content
    assert "<html" in content
    assert "<head>" in content
    assert "</head>" in content
    assert "<body>" in content
    assert "</body>" in content
    assert "</html>" in content


def test_generate_landing_page_has_title_tag(tmp_path):
    """Test that the generated HTML has a title tag with the product name."""
    name = "My Product"
    description = "Description"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    assert "<title>My Product</title>" in content


def test_generate_landing_page_default_output_path(tmp_path):
    """Test that generate_landing_page uses current directory by default."""
    import os
    original_cwd = os.getcwd()

    try:
        # Change to tmp_path
        os.chdir(tmp_path)

        name = "Test"
        description = "Test"

        output_file = generate_landing_page(name, description)

        # Should create in current directory (tmp_path)
        assert output_file.name == "index.html"
        assert output_file.exists()
        # Verify it's in the current directory
        assert (tmp_path / "index.html").exists()
    finally:
        os.chdir(original_cwd)


def test_cli_landing_page_command_creates_html(tmp_path):
    """Test that the CLI landing-page command creates index.html."""
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            cli,
            ["landing-page", "--name", "My Tool", "--desc", "Awesome tool"]
        )

        assert result.exit_code == 0
        assert "Generating landing page for: My Tool" in result.output
        assert "Landing page created at:" in result.output

        # Check that file was created
        index_file = Path("index.html")
        assert index_file.exists()

        # Verify content
        content = index_file.read_text()
        assert "<h1>My Tool</h1>" in content
        assert "<p>Awesome tool</p>" in content
        assert "<button>Get Started</button>" in content


def test_cli_landing_page_command_with_custom_output(tmp_path):
    """Test that the CLI landing-page command accepts custom output directory."""
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create a custom output directory
        output_dir = Path("custom_output")
        output_dir.mkdir()

        result = runner.invoke(
            cli,
            [
                "landing-page",
                "--name", "Test Product",
                "--desc", "Test Description",
                "--output", "custom_output"
            ]
        )

        assert result.exit_code == 0

        # Check that file was created in custom directory
        index_file = output_dir / "index.html"
        assert index_file.exists()


def test_cli_landing_page_command_requires_name(tmp_path):
    """Test that the CLI landing-page command requires --name option."""
    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["landing-page", "--desc", "Test Description"]
    )

    assert result.exit_code != 0
    assert "Missing option '--name'" in result.output


def test_cli_landing_page_command_requires_desc(tmp_path):
    """Test that the CLI landing-page command requires --desc option."""
    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["landing-page", "--name", "Test Product"]
    )

    assert result.exit_code != 0
    assert "Missing option '--desc'" in result.output


def test_generate_landing_page_with_special_characters(tmp_path):
    """Test that the landing page handles special characters correctly by escaping them."""
    name = "Tool & Service"
    description = "A tool with <special> \"characters\""

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    # Special characters should be escaped to prevent XSS
    assert "Tool &amp; Service" in content
    assert "&lt;special&gt;" in content
    assert "&quot;characters&quot;" in content


def test_generate_landing_page_prevents_xss(tmp_path):
    """Test that the landing page prevents XSS attacks by escaping malicious input."""
    name = "<script>alert(1)</script>"
    description = "<img src=x onerror=alert(1)>"

    output_file = generate_landing_page(name, description, str(tmp_path))
    content = output_file.read_text()

    # Malicious tags should be escaped, not executed
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in content
    assert "&lt;img src=x onerror=alert(1)&gt;" in content

    # Raw script/img tags should NOT appear in the output
    assert "<script>alert(1)</script>" not in content
    assert "<img src=x onerror=alert(1)>" not in content


def test_generate_landing_page_validates_empty_name(tmp_path):
    """Test that generate_landing_page raises ValueError for empty name."""
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace-only"):
        generate_landing_page("", "Valid description", str(tmp_path))


def test_generate_landing_page_validates_whitespace_name(tmp_path):
    """Test that generate_landing_page raises ValueError for whitespace-only name."""
    with pytest.raises(ValueError, match="Name cannot be empty or whitespace-only"):
        generate_landing_page("   ", "Valid description", str(tmp_path))


def test_generate_landing_page_validates_empty_description(tmp_path):
    """Test that generate_landing_page raises ValueError for empty description."""
    with pytest.raises(ValueError, match="Description cannot be empty or whitespace-only"):
        generate_landing_page("Valid name", "", str(tmp_path))


def test_generate_landing_page_validates_whitespace_description(tmp_path):
    """Test that generate_landing_page raises ValueError for whitespace-only description."""
    with pytest.raises(ValueError, match="Description cannot be empty or whitespace-only"):
        generate_landing_page("Valid name", "   ", str(tmp_path))
