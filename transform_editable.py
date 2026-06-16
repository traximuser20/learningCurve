
import re
import sys
import os

def transform_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # LearnWorlds standard button pattern: <a> with span inside
    # Find <a> tags with learnworlds-button and ensure they have the pattern
    def btn_pattern_fix(match):
        full_tag = match.group(0)
        # If it's already a learnworlds-button and doesn't have the span yet
        if 'learnworlds-button' in full_tag and '<span' not in full_tag:
            # Extract content between <a> and </a>
            content_match = re.search(r'>(.*?)</a>', full_tag, re.S)
            if content_match:
                inner_text = content_match.group(1).strip()
                # Replace with span pattern
                new_inner = f'<span class="learnworlds-element learnworlds-text" data-node-type="text" contenteditable="" tabindex="0">{inner_text}</span>'
                return full_tag.replace(inner_text, new_inner).replace('data-node-type="button"', 'data-node-type="button" contenteditable="false"')
        return full_tag

    # 1. Add basic attributes to headers, paragraphs, spans, and list items
    def add_edit_attrs(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        
        # Skip if already has attributes
        if 'contenteditable' in attrs:
            return match.group(0)
            
        # Determine class injection
        lw_class = "learnworlds-text"
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            lw_class = "learnworlds-heading"
        
        if 'class="' in attrs:
            attrs = attrs.replace('class="', f'class="learnworlds-element {lw_class} ')
        else:
            attrs = f' class="learnworlds-element {lw_class}"' + attrs
            
        attrs += ' data-node-type="text" contenteditable="" tabindex="0"'
        return f'<{tag}{attrs}'

    # Target leaf nodes primarily
    content = re.sub(r'<(h1|h2|h3|h4|h5|h6|p|li|span|div class="stat-val[^"]*")\b(\s+[^>]*)?', add_edit_attrs, content)

    # 2. Fix buttons (standard LW pattern)
    content = re.sub(r'<a\s+[^>]*learnworlds-button[^>]*>.*?</a>', btn_pattern_fix, content, flags=re.S)

    # 3. Ensure images are editable
    def img_fix(match):
        attrs = match.group(1) or ""
        if 'learnworlds-image' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-image learnworlds-element js-change-image-node ')
            else:
                attrs = ' class="learnworlds-image learnworlds-element js-change-image-node"' + attrs
        if 'data-node-type="image"' not in attrs:
            attrs += ' data-node-type="image"'
        if 'tabindex="0"' not in attrs:
            attrs += ' tabindex="0"'
        return f'<img{attrs}'

    content = re.sub(r'<img\b(\s+[^>]*)?', img_fix, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python transform_editable.py <input> <output>")
    else:
        transform_file(sys.argv[1], sys.argv[2])
