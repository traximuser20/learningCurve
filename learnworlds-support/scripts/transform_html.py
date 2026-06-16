import re
import os
import sys

def add_lw_attributes(html):
    # h1-h6
    def h_repl(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-heading ')
            else:
                attrs = f' class="learnworlds-element learnworlds-heading"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="text"'
        if 'contenteditable' not in attrs:
            attrs += ' contenteditable="true"'
        return f'<{tag}{attrs}>{content}</{tag}>'
    html = re.sub(r'<(h[1-6])\b([^>]*)>(.*?)</\1>', h_repl, html, flags=re.S)
    
    # p
    def p_repl(match):
        attrs = match.group(1) or ""
        content = match.group(2)
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-text ')
            else:
                attrs = f' class="learnworlds-element learnworlds-text"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="text"'
        if 'contenteditable' not in attrs:
            attrs += ' contenteditable="true"'
        return f'<p{attrs}>{content}</p>'
    html = re.sub(r'<p\b([^>]*)>(.*?)</p>', p_repl, html, flags=re.S)

    # a/buttons
    def a_repl(match):
        attrs = match.group(1) or ""
        content = match.group(2)
        is_button = 'btn' in attrs
        lw_class = 'learnworlds-button' if is_button else 'learnworlds-text'
        node_type = 'button' if is_button else 'text'
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', f'class="learnworlds-element {lw_class} ')
            else:
                attrs = f' class="learnworlds-element {lw_class}"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += f' data-node-type="{node_type}"'
        if 'contenteditable' not in attrs:
            attrs += ' contenteditable="true"'
        return f'<a{attrs}>{content}</a>'
    html = re.sub(r'<a\b([^>]*)>(.*?)</a>', a_repl, html, flags=re.S)
    
    # images
    def img_repl(match):
        attrs = match.group(1) or ""
        attrs = attrs.rstrip(' /')
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-image ')
            else:
                attrs = f' class="learnworlds-element learnworlds-image"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="image"'
        return f'<img{attrs} />'
    html = re.sub(r'<img\b([^>]*)>', img_repl, html)
    
    return html

def transform(input_file, output_file, section_id="custom_section"):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Body HTML
    body_match = re.search(r'<body>(.*?)<script>', content, re.S)
    if not body_match:
        body_match = re.search(r'<body>(.*?)</body>', content, re.S)
    
    html_content = body_match.group(1).strip() if body_match else ""
    html_content = add_lw_attributes(html_content)

    final_html = f"""
<section class="js-learnworlds-section learnworlds-section lw-brand-bg stretched-bg learnworlds-size-normal learnworlds-align-center js-change-image-node"
         data-section-id="{section_id}"
         id="{section_id}">
    <div class="js-video-wrapper"></div>
    <div class="learnworlds-section-overlay lw-light-bg js-learnworlds-overlay" style="display: none"></div>
    <div class="learnworlds-section-content js-learnworlds-section-content wide">
        <div class="lw-wrapper">
            {html_content}
        </div>
    </div>
</section>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Transformation complete: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python transform_html.py <input.html> <output.html> [section_id]")
    else:
        sid = sys.argv[3] if len(sys.argv) > 3 else "custom_section"
        transform(sys.argv[1], sys.argv[2], sid)
