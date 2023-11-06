import mistune, chardet, pkg_resources
from bs4 import BeautifulSoup
from pygments.formatters import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {content}
    <script>hljs.highlightAll();</script>
</body>
</html>
"""

# Create a custom renderer for Mistune to handle code highlighting with Pygments
class HighlightRenderer(mistune.HTMLRenderer):
    def render_block_code(self, text, info=None):  # Adjusted here to add `info`
        print(text, info)
        if not info:
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(text)
        lexer = get_lexer_by_name(info, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def convert_md_to_html(md_filename, html_filename, mode="dark"):
    # Load the markdown content
    rawdata = open(md_filename, "rb").read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Load markdown content with detected encoding
    with open(md_filename, 'r', encoding=encoding) as md_file:
        md_content = md_file.read()

    # Initialize mistune with the custom renderer
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)

    # Convert markdown to HTML
    html_content = markdown(md_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in headers:
        header['id'] = header.text.lower().replace(" ", "-")
    title = soup.find('h1').text

    # Update the content with the processed HTML
    html_content = str(soup)

    # Include the content in the HTML template
    css_path = f"mdhub/models/{mode}.css"
    css_content = pkg_resources.resource_string(__name__, css_path).decode('utf-8')
    full_html = HTML_TEMPLATE.format(
        title=title, 
        css=css_content, 
        content=html_content, 
    )
    soup = BeautifulSoup(full_html, 'html.parser')
    pretty_html = soup.prettify()

    # Write the full HTML to the output file
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(pretty_html)

# Example usage
# convert_md_to_html('README.md', 'readme.html', mode='dark')
