"""Landing page template generator for AgenticStarter."""

from pathlib import Path
import html


def generate_landing_page(product_name, description, output_file='index.html'):
    """
    Generate a static HTML landing page.

    Args:
        product_name: Name of the product
        description: Product description
        output_file: Output HTML file path
    """
    # Escape user inputs to prevent XSS attacks
    escaped_name = html.escape(product_name)
    escaped_desc = html.escape(description)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{escaped_desc}">
    <title>{escaped_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            background: white;
            padding: 60px 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}
        h1 {{
            font-size: 3em;
            color: #333;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 40px;
            line-height: 1.8;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 48px;
            font-size: 1.1em;
            font-weight: 600;
            text-decoration: none;
            border-radius: 50px;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{escaped_name}</h1>
        <p>{escaped_desc}</p>
        <a href="#" class="cta-button">Get Started</a>
    </div>
</body>
</html>
'''

    Path(output_file).write_text(html_content)
    return output_file
