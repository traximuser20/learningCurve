import re
from bs4 import BeautifulSoup

def fix_html_structure(file_path):
    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Tags that MUST NOT be contenteditable
    container_tags = ['a', 'button', 'div', 'section', 'nav', 'ul', 'li', 'table', 'tr', 'thead', 'tbody']
    
    # 1. Strip all editability from everything
    for tag in soup.find_all(True):
        if tag.has_attr('contenteditable'):
            del tag['contenteditable']
        if tag.has_attr('tabindex'):
            del tag['tabindex']

    # 2. Re-apply to leaf text nodes ONLY
    # Leaf text nodes: p, h1-h5, span
    leaf_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span']
    
    for tag in soup.find_all(leaf_tags):
        # Only if it has the right node type and is not nested inside a forbidden container
        if tag.get('data-node-type') == 'text':
            # Check if it's inside a forbidden container (simple check)
            if tag.parent.name not in container_tags:
                tag['contenteditable'] = ""
                tag['tabindex'] = "0"

    with open(file_path, 'w') as f:
        f.write(str(soup))
    print(f"Structure fixed for {file_path}")

fix_html_structure('learnWorlds/dist/section_html.html')
