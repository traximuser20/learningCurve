
import re
import sys

def transform_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up potential duplicate attributes from previous runs
    content = re.sub(r'(class="[^"]*)learnworlds-element learnworlds-(text|heading) [^"]*', r'\1', content)
    content = re.sub(r'\s+data-node-type="[^"]*"', '', content)
    content = re.sub(r'\s+contenteditable="[^"]*"', '', content)
    content = re.sub(r'\s+tabindex="[^"]*"', '', content)
    
    # 2. Identify text nodes (headers, paragraphs, spans, li)
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
    # First, find all <a> tags that look like buttons
    def btn_repl(match):
        full_tag = match.group(0)
        attrs = match.group(1) or ""
        inner_content = match.group(2)
        
        # Injection of classes to <a>
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-button learnworlds-element ')
        else:
            attrs = ' class="learnworlds-button learnworlds-element"' + attrs
        
        # <a> should not be contenteditable, but span inside should be
        attrs += ' data-node-type="button" contenteditable="false"'
        
        # Clean up inner content if it already has tags
        clean_inner = re.sub(r'<[^>]+>', '', inner_content).strip()
        
        new_inner = f'<span class="learnworlds-element learnworlds-text" data-node-type="text" contenteditable="" tabindex="0">{clean_inner}</span>'
        return f'<a{attrs}>{new_inner}</a>'

    # Match <a> tags that have 'btn' in their class
    content = re.sub(r'<a\b([^>]*class="[^"]*btn[^"]*"[^>]*)>(.*?)</a>', btn_repl, content, flags=re.S)

    # 5. Handle trust-items (which are divs with text)
    def div_text_repl(match):
        attrs = match.group(1) or ""
        inner = match.group(2)
        if 'trust-item' in attrs or 'feat-cell' in attrs:
            # We want to make the text inside editable if it's raw text
            # This is tricky with regex, but let's try wrapping raw text in spans
            pass
        return match.group(0)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    transform_file(sys.argv[1], sys.argv[2])
