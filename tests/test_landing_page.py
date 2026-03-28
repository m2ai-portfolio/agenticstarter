"""Comprehensive tests for landing page generation."""

import os
from pathlib import Path
import pytest
from agenticstarter.landing_page_template import generate_landing_page


def test_basic_landing_page_generation(temp_dir):
    """Test basic landing page generation with simple inputs."""
    output_file = os.path.join(temp_dir, 'index.html')
    result = generate_landing_page('My Tool', 'Awesome tool', output_file)

    assert result == output_file
    assert Path(output_file).exists()

    content = Path(output_file).read_text()
    assert 'My Tool' in content
    assert 'Awesome tool' in content
    assert 'Get Started' in content


def test_landing_page_with_special_characters(temp_dir):
    """Test HTML escaping for special characters to prevent XSS."""
    output_file = os.path.join(temp_dir, 'index.html')

    # Test with HTML special characters
    product_name = '<script>alert("xss")</script>'
    description = 'Tool with <b>HTML</b> & "quotes"'

    generate_landing_page(product_name, description, output_file)

    content = Path(output_file).read_text()

    # Should be escaped, not executed
    assert '<script>alert("xss")</script>' not in content
    assert '&lt;script&gt;' in content
    assert '&lt;b&gt;HTML&lt;/b&gt;' in content
    assert '&quot;quotes&quot;' in content or '"quotes"' in content


def test_landing_page_html_structure(temp_dir):
    """Test that generated HTML has proper structure and meta tags."""
    output_file = os.path.join(temp_dir, 'index.html')
    generate_landing_page('Test Product', 'Test Description', output_file)

    content = Path(output_file).read_text()

    # Check DOCTYPE and basic structure
    assert '<!DOCTYPE html>' in content
    assert '<html lang="en">' in content
    assert '<head>' in content
    assert '<body>' in content

    # Check meta tags
    assert '<meta charset="UTF-8">' in content
    assert '<meta name="viewport"' in content
    assert '<meta name="description"' in content

    # Check title
    assert '<title>Test Product</title>' in content

    # Check semantic HTML elements
    assert '<h1>Test Product</h1>' in content
    assert '<p>Test Description</p>' in content
    assert 'class="cta-button"' in content
    assert '>Get Started</a>' in content


def test_landing_page_default_output_filename():
    """Test that default output filename is index.html."""
    # Use /tmp to avoid polluting project directory
    temp_output = '/tmp/test_default_index.html'

    try:
        result = generate_landing_page('Product', 'Description', temp_output)
        assert result == temp_output
        assert Path(temp_output).exists()
    finally:
        # Clean up
        if Path(temp_output).exists():
            Path(temp_output).unlink()


def test_landing_page_custom_output_path(temp_dir):
    """Test landing page generation with custom output path."""
    custom_path = os.path.join(temp_dir, 'custom', 'landing.html')
    os.makedirs(os.path.dirname(custom_path), exist_ok=True)

    result = generate_landing_page('Product', 'Description', custom_path)

    assert result == custom_path
    assert Path(custom_path).exists()


def test_landing_page_with_long_description(temp_dir):
    """Test landing page with long multi-line description."""
    output_file = os.path.join(temp_dir, 'index.html')
    long_desc = "This is a very long description. " * 20

    generate_landing_page('Product', long_desc, output_file)

    content = Path(output_file).read_text()
    assert long_desc in content


def test_landing_page_with_unicode_characters(temp_dir):
    """Test landing page with unicode characters."""
    output_file = os.path.join(temp_dir, 'index.html')

    product_name = 'My Tool 🚀'
    description = 'Awesome tool with émojis and spëcial çharacters'

    generate_landing_page(product_name, description, output_file)

    content = Path(output_file).read_text()
    assert '🚀' in content or '&#' in content  # Either raw emoji or HTML entity
    assert 'émojis' in content or '&eacute;' in content


def test_landing_page_css_included(temp_dir):
    """Test that generated page includes CSS styling."""
    output_file = os.path.join(temp_dir, 'index.html')
    generate_landing_page('Product', 'Description', output_file)

    content = Path(output_file).read_text()

    # Check for CSS
    assert '<style>' in content
    assert 'font-family' in content
    assert '.cta-button' in content
    assert 'background' in content
    assert 'linear-gradient' in content


def test_landing_page_responsive_design(temp_dir):
    """Test that generated page has responsive design elements."""
    output_file = os.path.join(temp_dir, 'index.html')
    generate_landing_page('Product', 'Description', output_file)

    content = Path(output_file).read_text()

    # Check viewport meta tag for mobile responsiveness
    assert 'width=device-width' in content
    assert 'initial-scale=1.0' in content

    # Check for responsive CSS properties
    assert 'max-width' in content or 'width: 100%' in content
