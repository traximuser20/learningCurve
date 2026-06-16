
import re
import sys

def transform_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Strip ALL LW attributes and classes to start clean
    content = re.sub(r'\s+data-node-type="[^"]*"', '', content)
    content = re.sub(r'\s+contenteditable="[^"]*"', '', content)
    content = re.sub(r'\s+tabindex="[^"]*"', '', content)
    content = re.sub(r'\s+data-magic="[^"]*"', '', content)
    
    # Clean classes
    def clean_classes(match):
        attrs = match.group(0)
        attrs = re.sub(r'\s*learnworlds-element\s*', ' ', attrs)
        attrs = re.sub(r'\s*learnworlds-text\s*', ' ', attrs)
        attrs = re.sub(r'\s*learnworlds-heading\s*', ' ', attrs)
        attrs = re.sub(r'\s*learnworlds-button\s*', ' ', attrs)
        attrs = re.sub(r'\s*learnworlds-image\s*', ' ', attrs)
        attrs = re.sub(r'\s*js-change-image-node\s*', ' ', attrs)
        return attrs
    
    content = re.sub(r'class="[^"]*"', clean_classes, content)

    # 2. Add attributes to text nodes (headers, paragraphs, spans, li)
    def text_repl(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        
        lw_class = "learnworlds-text"
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            lw_class = "learnworlds-heading"
            
        if 'class="' in attrs:
            attrs = attrs.replace('class="', f'class="learnworlds-element {lw_class} ')
        else:
            attrs = f' class="learnworlds-element {lw_class}"' + attrs
            
        attrs += ' data-node-type="text" contenteditable="" tabindex="0"'
        return f'<{tag}{attrs}'

    content = re.sub(r'<(h1|h2|h3|h4|h5|h6|p|li|span)\b(\s+[^>]*)?', text_repl, content)

    # 3. Handle images
    def img_repl(match):
        attrs = match.group(1) or ""
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-image learnworlds-element js-change-image-node ')
        else:
            attrs = ' class="learnworlds-image learnworlds-element js-change-image-node"' + attrs
        attrs += ' data-node-type="image" tabindex="0"'
        return f'<img{attrs}'

    content = re.sub(r'<img\b(\s+[^>]*)?', img_repl, content)

    # 4. Handle buttons (<a> with nested <span>)
    def btn_repl(match):
        attrs = match.group(1) or ""
        inner_content = match.group(2)
        
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-button learnworlds-element ')
        else:
            attrs = ' class="learnworlds-button learnworlds-element"' + attrs
        
        attrs += ' data-node-type="button" contenteditable="false"'
        
        # Strip internal spans if they were added previously
        clean_inner = re.sub(r'<span class="learnworlds-element learnworlds-text"[^>]*>(.*?)</span>', r'\1', inner_content, flags=re.S)
        clean_inner = re.sub(r'<[^>]+>', '', clean_inner).strip()
        
        new_inner = f'<span class="learnworlds-element learnworlds-text" data-node-type="text" contenteditable="" tabindex="0">{clean_inner}</span>'
        return f'<a{attrs}>{new_inner}</a>'

    # Match all <a> tags (links and buttons)
    content = re.sub(r'<a\b([^>]*)>(.*?)</a>', btn_repl, content, flags=re.S)

    # 5. Handle logos specially (don't want to wrap them in buttons usually if they are logo class)
    # But for LW, a logo is just an <a> tag. Let's make sure it doesn't get double spanned.

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    transform_file(sys.argv[1], sys.argv[2])
