
import re
import os

input_path = '/home/arch/Documents/CaseClinical/src/ClaudeCode.html'
output_path = '/home/arch/Documents/CaseClinical/learnWorlds/ClaudeCode.html'

with open(input_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract Google Fonts links
fonts_match = re.search(r'(<link rel="preconnect" href="https://fonts.googleapis.com" />\s*<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\s*<link\s+href="https://fonts.googleapis.com/css2\?family=Sora:wght@300;400;500;600;700;800&family=DM\+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap"\s+rel="stylesheet"\s*/>)', content, re.S)
fonts = fonts_match.group(1) if fonts_match else ''

# 2. Extract style blocks
styles = re.findall(r'(<style>.*?</style>)', content, re.S)
styles_joined = "\n".join(styles)

# Add Visibility Force CSS
visibility_fix = """
<style>
/* Visibility Force for LearnWorlds Preview */
[data-reveal] {
    opacity: 1 !important;
    transform: none !important;
}
.navbar {
    background: rgba(255, 255, 255, 0.95) !important;
}
</style>
"""
styles_joined += visibility_fix

# 3. Extract body content and final script
body_match = re.search(r'<body>(.*?)<script>(.*?)</script>\s*</body>', content, re.S)
if not body_match:
    body_content_match = re.search(r'<body>(.*?)</body>', content, re.S)
    body_content_full = body_content_match.group(1) if body_content_match else ''
    script_match = re.search(r'<script>(.*?)</script>\s*</body>', content, re.S)
    script_content = script_match.group(1) if script_match else ''
    body_content = re.sub(r'<script>.*?</script>', '', body_content_full, flags=re.S).strip()
else:
    body_content = body_match.group(1).strip()
    script_content = body_match.group(2).strip()

# Remove data-reveal from main section tags
body_content = re.sub(r'(<section[^>]+)data-reveal', r'\1', body_content)

def add_attributes(html):
    # h1 and h2
    def h_repl(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        is_hero_title = 'hero-title' in attrs
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-heading ')
        else:
            attrs = f' class="learnworlds-element learnworlds-heading"{attrs}'
        attrs += ' data-node-type="text" contenteditable=""'
        if is_hero_title:
            attrs += ' data-magic="title"'
        return f'<{tag}{attrs}'

    html = re.sub(r'<(h1|h2)\b(\s+[^>]*)?', h_repl, html)

    # p
    def p_repl(match):
        attrs = match.group(1) or ""
        is_hero_desc = 'hero-desc' in attrs
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-element ')
        else:
            attrs = f' class="learnworlds-element"{attrs}'
        attrs += ' data-node-type="text" contenteditable=""'
        if is_hero_desc:
            attrs += ' data-magic="description"'
        return f'<p{attrs}'

    html = re.sub(r'<p\b(\s+[^>]*)?', p_repl, html)

    # a with class="btn"
    def a_repl(match):
        attrs = match.group(1) or ""
        if 'class="' in attrs and 'btn' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-button learnworlds-element ')
            attrs += ' data-node-type="button"'
        return f'<a{attrs}'

    html = re.sub(r'<a\b(\s+[^>]*)?', a_repl, html)

    # img
    def img_repl(match):
        attrs = match.group(1) or ""
        is_self_closing = attrs.endswith('/')
        if is_self_closing:
            attrs = attrs[:-1]
        if 'class="' in attrs:
            attrs = attrs.replace('class="', 'class="learnworlds-image learnworlds-element ')
        else:
            attrs = f' class="learnworlds-image learnworlds-element"{attrs}'
        attrs += ' data-node-type="image"'
        if is_self_closing:
            return f'<img{attrs} />'
        else:
            return f'<img{attrs}'

    html = re.sub(r'<img\b(\s+[^>]*)?', img_repl, html)
    return html

body_content_modified = add_attributes(body_content)

final_output = f"""{fonts}
{styles_joined}

<section class="js-learnworlds-section learnworlds-section lw-brand-bg stretched-bg learnworlds-size-normal learnworlds-align-center js-change-image-node"
         data-section-id="tpl_claudecode"
         id="section_claudecode">
    <div class="js-video-wrapper"></div>
    <div class="learnworlds-section-overlay lw-light-bg js-learnworlds-overlay" style="display: none"></div>
    <div class="learnworlds-section-content js-learnworlds-section-content wide">
        {body_content_modified}
    </div>
</section>

<script>
{script_content}
</script>
"""

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_output)

print(f"File created at {output_path}")
