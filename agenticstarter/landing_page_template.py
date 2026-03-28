"""
Landing page generator for AgenticStarter (Feature 2)
"""

import html
from pathlib import Path


def generate_landing_page(name: str, description: str, output_path: str = ".") -> Path:
    """
    Generate a static HTML landing page for a micro-SaaS product.

    Args:
        name: The product name to display in the heading and title
        description: The product description to display in the paragraph
        output_path: Directory where index.html should be created (default: current directory)

    Returns:
        Path to the created index.html file

    Raises:
        ValueError: If name or description is empty or whitespace-only
    """
    # Input validation
    if not name or not name.strip():
        raise ValueError("Name cannot be empty or whitespace-only")
    if not description or not description.strip():
        raise ValueError("Description cannot be empty or whitespace-only")

    # Sanitize user input to prevent XSS attacks
    safe_name = html.escape(name)
    safe_description = html.escape(description)
    # Use quote=True for HTML attribute values
    safe_description_attr = html.escape(description, quote=True)

    output_dir = Path(output_path)
    output_file = output_dir / "index.html"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{safe_description_attr}">
    <title>{safe_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}

        .container {{
            background: white;
            border-radius: 16px;
            padding: 60px 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}

        h1 {{
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 20px;
            font-weight: 700;
        }}

        p {{
            font-size: 1.2rem;
            color: #4a5568;
            margin-bottom: 30px;
            line-height: 1.8;
        }}

        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}

        button:active {{
            transform: translateY(0);
        }}

        @media (max-width: 600px) {{
            .container {{
                padding: 40px 20px;
            }}

            h1 {{
                font-size: 2rem;
            }}

            p {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{safe_name}</h1>
        <p>{safe_description}</p>
        <button>Get Started</button>
    </div>
</body>
</html>"""

    output_file.write_text(html_content)
    return output_file
