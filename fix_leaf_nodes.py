import re

def fix_html(file_path):
    with open(file_path, 'r') as f:
        html = f.read()

    # Leaf nodes that should be editable
    leaf_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'span']
    
    # 1. Strip all existing contenteditable/tabindex
    html = re.sub(r'\s+contenteditable=["\'][^"\']*["\']', '', html)
    html = re.sub(r'\s+tabindex=["\'][^"\']*["\']', '', html)
    
    # 2. Re-apply to leaf nodes that have data-node-type
    def add_attrs(match):
        tag = match.group(1)
        attrs = match.group(2)
        if 'data-node-type' in attrs:
            attrs += ' contenteditable="" tabindex="0"'
        return f'<{tag}{attrs}>'
        
    for tag in leaf_tags:
        # Matches <tag attrs>
        html = re.sub(r'<' + tag + r'\s+([^>]*?)>', add_attrs, html)
        
    with open(file_path, 'w') as f:
        f.write(html)
    print(f"Fixed {file_path}")

fix_html('learnWorlds/dist/section_html.html')
