import re
import os

def add_lw_attributes(html):
    # 1. Headings h1-h6
    def h_repl(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-heading learnworlds-element ')
            else:
                attrs = f' class="learnworlds-heading learnworlds-element"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="text"'
        attrs += ' contenteditable="" tabindex="0"'
        return f'<{tag}{attrs}>{content}</{tag}>'
    html = re.sub(r'<(h[1-6])\b([^>]*)>(.*?)</\1>', h_repl, html, flags=re.S)
    
    # 2. Paragraphs
    def p_repl(match):
        attrs = match.group(1) or ""
        content = match.group(2)
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-text learnworlds-element ')
            else:
                attrs = f' class="learnworlds-text learnworlds-element"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="text"'
        attrs += ' contenteditable="" tabindex="0"'
        return f'<p{attrs}>{content}</p>'
    html = re.sub(r'<p\b([^>]*)>(.*?)</p>', p_repl, html, flags=re.S)

    # 3. Buttons (a tags with btn or nav-signin classes)
    def a_repl(match):
        attrs = match.group(1) or ""
        content = match.group(2)
        is_button = 'btn' in attrs or 'nav-signin' in attrs
        
        if is_button:
            if 'learnworlds-element' not in attrs:
                if 'class="' in attrs:
                    attrs = attrs.replace('class="', 'class="learnworlds-button learnworlds-element ')
                else:
                    attrs = f' class="learnworlds-button learnworlds-element"{attrs}'
            if 'data-node-type' not in attrs:
                attrs += ' data-node-type="button"'
            attrs += ' contenteditable="false" tabindex="0"'
            # Wrap content in editable span
            new_content = f'<span class="learnworlds-element learnworlds-text" data-node-type="text" contenteditable="" tabindex="0">{content}</span>'
            return f'<a{attrs}>{new_content}</a>'
        else:
            # Normal text link
            if 'learnworlds-element' not in attrs:
                if 'class="' in attrs:
                    attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-text ')
                else:
                    attrs = f' class="learnworlds-element learnworlds-text"{attrs}'
            if 'data-node-type' not in attrs:
                attrs += ' data-node-type="text"'
            attrs += ' contenteditable="" tabindex="0"'
            return f'<a{attrs}>{content}</a>'
    html = re.sub(r'<a\b([^>]*)>(.*?)</a>', a_repl, html, flags=re.S)

    # 4. Images
    def img_repl(match):
        attrs = match.group(1) or ""
        attrs = attrs.rstrip(' /')
        if 'learnworlds-element' not in attrs:
            if 'class="' in attrs:
                attrs = attrs.replace('class="', 'class="learnworlds-image learnworlds-element js-change-image-node ')
            else:
                attrs = f' class="learnworlds-image learnworlds-element js-change-image-node"{attrs}'
        if 'data-node-type' not in attrs:
            attrs += ' data-node-type="image"'
        attrs += ' contenteditable="false" tabindex="0"'
        return f'<img{attrs} />'
    html = re.sub(r'<img\b([^>]*)>', img_repl, html)

    # 5. List items, spans, and text-only divs (leaf nodes)
    def leaf_repl(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        # Only make editable if it has text and NO tags inside
        if content.strip() and '<' not in content:
            if 'learnworlds-element' not in attrs:
                if 'class="' in attrs:
                    attrs = attrs.replace('class="', 'class="learnworlds-element learnworlds-text ')
                else:
                    attrs = f' class="learnworlds-element learnworlds-text"{attrs}'
            if 'data-node-type' not in attrs:
                attrs += ' data-node-type="text"'
            if 'contenteditable' not in attrs:
                attrs += ' contenteditable=""'
            if 'tabindex' not in attrs:
                attrs += ' tabindex="0"'
        return f'<{tag}{attrs}>{content}</{tag}>'
    html = re.sub(r'<(li|span|th|td|div)\b([^>]*)>(.*?)</\1>', leaf_repl, html, flags=re.S)
    
    return html

def transform():
    with open('src/ClaudeCode.html', 'r') as f:
        content = f.read()

    # Extract Google Fonts links
    fonts_match = re.search(r'(<link rel="preconnect" href="https://fonts.googleapis.com" />\s*<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\s*<link\s+href="https://fonts.googleapis.com/css2\?family=Sora:wght@300;400;500;600;700;800&family=DM\+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap"\s+rel="stylesheet"\s*/>)', content, re.S)
    fonts = fonts_match.group(1) if fonts_match else ''

    # Extract CSS
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.S)
    css_content = "\n".join(style_blocks)
    
    # LW Platform Overrides & Reset
    overrides = """
/* LW Platform Overrides */
.lw-caseclinical-wrapper {
    width: 100vw !important;
    max-width: 100vw !important;
    position: relative !important;
    left: 50% !important;
    margin-left: -50vw !important;
    display: block !important;
    overflow: visible !important;
    background: #ffffff !important;
}

/* Ensure LearnWorlds section container allows full width */
:is(.learnworlds-section, .learnworlds-section-content, .js-learnworlds-section-content):has(.lw-caseclinical-wrapper) {
    width: 100% !important;
    max-width: none !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: visible !important;
}

/* Fix for editor interaction */
.lw-caseclinical-wrapper .learnworlds-element {
    pointer-events: auto !important;
}

/* Force absolute positioning in editor to prevent blocking */
.learnworlds-editor .lw-caseclinical-wrapper .lw-navbar {
    position: absolute !important;
}

/* Force visibility of all elements in the editor */
.lw-caseclinical-wrapper [data-reveal] {
    opacity: 1 !important;
    transform: none !important;
}

.lw-caseclinical-wrapper .lw-navbar {
    position: fixed !important;
    width: 100% !important;
    left: 0 !important;
    top: 0 !important;
    z-index: 9999 !important;
    background: rgba(255, 255, 255, 0.95) !important;
}

.lw-caseclinical-wrapper .lw-navbar.scrolled {
    padding: 10px 0 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
}
"""
    css_content = css_content.replace(':root', '.lw-caseclinical-wrapper')
    css_content = re.sub(r'(html|body|\*)\s*\{[^}]*\}', '', css_content)
    css_content = css_content.replace('.navbar', '.lw-navbar')
    css_content = css_content.replace('.navbar-inner', '.lw-navbar-inner')
    css_content = overrides + "\n" + css_content

    # Extract Body HTML
    body_match = re.search(r'<body>(.*?)<script>', content, re.S)
    html_content = body_match.group(1).strip() if body_match else ""

    # Renames for LW compatibility
    html_content = html_content.replace('class="navbar"', 'class="lw-navbar"')
    html_content = html_content.replace('id="navbar"', 'id="lw-navbar"')
    html_content = html_content.replace('class="container navbar-inner"', 'class="container lw-navbar-inner"')

    # Fix mockups values - Keep 0 for count-up animation
    html_content = re.sub(r'(<[^>]+class="[^"]*count-up[^"]*"[^>]*data-target="(\d+)"[^>]*>).*?(</[^>]+>)', 
                          r'\1 0 \3', html_content)

    # Fix Provider Portal card
    html_content = html_content.replace('<!-- Provider Portal -->\n          <div class="portal-card reverse"', 
                                      '<!-- Provider Portal -->\n          <div class="portal-card provider-fix"')

    # Add LearnWorlds attributes
    html_content = add_lw_attributes(html_content)

    # Extract Script - Surgically extract only hamburger and nav link logic
    script_match = re.search(r'<script>(.*?)</script>', content, re.S)
    original_js = script_match.group(1).strip() if script_match else ""
    
    # Extract only hamburger and active link logic
    js_parts = []
    
    # Hamburger logic
    hamburger_match = re.search(r'// ─── HAMBURGER.*?hamburger\.addEventListener.*?\s*\}\);', original_js, re.S)
    if hamburger_match:
        js_parts.append(hamburger_match.group(0))
        
    # Mobile menu links logic
    mobile_links_match = re.search(r'// Close mobile menu when a link is clicked.*?mobileMenuLinks\.forEach.*?\s*\}\);', original_js, re.S)
    if mobile_links_match:
        js_parts.append(mobile_links_match.group(0))
        
    # Active Nav Link logic
    active_nav_match = re.search(r'// ─── ACTIVE NAV LINK.*', original_js, re.S)
    if active_nav_match:
        js_parts.append(active_nav_match.group(0))
        
    js_content = "\n\n".join(js_parts)

    final_html = f"""
{fonts}

<section class="js-learnworlds-section learnworlds-section lw-brand-bg stretched-bg learnworlds-size-normal learnworlds-align-center js-change-image-node"
         data-section-id="section_claudecode"
         id="section_claudecode">
    <div class="js-video-wrapper"></div>
    <div class="learnworlds-section-overlay lw-light-bg js-learnworlds-overlay" style="display: none"></div>
    <div class="learnworlds-section-content js-learnworlds-section-content wide">
        <div class="lw-caseclinical-wrapper">
            {html_content}
        </div>
    </div>
</section>

    <script>
    (function() {{
        function init() {{
            console.log('CaseClinical: Initializing Animations...');
            const section = document.getElementById('section_claudecode');
            if (!section) return;

            // Navbar Scroll Logic
            const lwNavbar = document.getElementById('lw-navbar');
            if (lwNavbar) {{
                window.addEventListener('scroll', () => {{
                    if (window.scrollY > 50) {{
                        lwNavbar.classList.add('scrolled');
                    }} else {{
                        lwNavbar.classList.remove('scrolled');
                    }}
                }});
            }}

            // Force visibility of all reveal elements
            setTimeout(() => {{
                section.querySelectorAll('[data-reveal]').forEach(el => {{
                    el.classList.add('visible');
                    el.style.opacity = '1';
                    el.style.transform = 'none';
                }});
                
                // 1. Hero Mobile Mockup Progress Bar
                const phoneBar = section.querySelector('#phone-bar-fill');
                if (phoneBar) {{
                    phoneBar.style.width = '78%';
                }}

                // 2. Donut Charts (Hero & Portals)
                section.querySelectorAll('.donut-container').forEach(container => {{
                    const circles = container.querySelectorAll('.segment');
                    const radius = 45;
                    const circumference = 2 * Math.PI * radius;
                    let accumulatedPercent = 0;
                    
                    circles.forEach((circle, index) => {{
                        const percent = Number(circle.dataset.percent);
                        const dashLength = (percent / 100) * circumference;
                        const gapLength = circumference - dashLength;
                        
                        circle.style.strokeDasharray = `${{dashLength}} ${{gapLength}}`;
                        circle.style.strokeDashoffset = circumference;
                        
                        const offset = circumference * (1 - accumulatedPercent / 100);
                        accumulatedPercent += percent;
                        
                        setTimeout(() => {{
                            circle.style.strokeDashoffset = offset;
                        }}, index * 200 + 500);
                    }});
                }});

                // 3. Line Charts (Portals)
                section.querySelectorAll('.line-chart-svg').forEach(svg => {{
                    // Animate Lines
                    const paths = svg.querySelectorAll('.chart-line');
                    paths.forEach(path => {{
                        const length = path.getTotalLength();
                        path.style.strokeDasharray = length;
                        path.style.strokeDashoffset = length;
                        setTimeout(() => {{
                            path.style.strokeDashoffset = '0';
                        }}, 800);
                    }});
                    // Fade in Areas
                    const areas = svg.querySelectorAll('.chart-area');
                    areas.forEach(area => {{
                        area.style.opacity = '0';
                        area.style.transition = 'opacity 1.5s ease-in-out';
                        setTimeout(() => {{
                            area.style.opacity = '0.15';
                        }}, 1200);
                    }});
                }});

                // 4. Count Up numbers
                section.querySelectorAll('.count-up').forEach(el => {{
                    const target = parseInt(el.dataset.target);
                    if (isNaN(target)) return;
                    let start = 0;
                    const duration = 2000;
                    const startTime = performance.now();
                    
                    function animate(currentTime) {{
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const eased = 1 - Math.pow(1 - progress, 3);
                        el.textContent = Math.floor(eased * target).toLocaleString();
                        if (progress < 1) requestAnimationFrame(animate);
                        else el.textContent = target.toLocaleString();
                    }}
                    requestAnimationFrame(animate);
                }});

            }}, 600);

            {js_content}
        }}
        if (document.readyState === 'loading') {{ document.addEventListener('DOMContentLoaded', init); }}
        else {{ setTimeout(init, 300); }}
    }})();
    </script>
"""

    os.makedirs('learnWorlds/dist', exist_ok=True)
    with open('learnWorlds/dist/site_custom_code.css', 'w') as f:
        f.write(css_content)
    with open('learnWorlds/dist/section_html.html', 'w') as f:
        f.write(final_html)
    
    print("Full Transformation complete.")

if __name__ == "__main__":
    transform()