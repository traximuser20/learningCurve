import re
with open('src/ClaudeCode.html', 'r') as f:
    content = f.read()
body_match = re.search(r'<body>(.*?)<script>', content, re.S)
if body_match:
    html_content = body_match.group(1).strip()
    print(f"Length of html_content: {len(html_content)}")
    print("Navbar in html_content:", "navbar" in html_content)
    print("Features Strip in html_content:", "features-strip" in html_content)
    print("Ecosystem in html_content:", "ecosystem" in html_content)
    print("Why in html_content:", "why" in html_content)
    print("Logos in html_content:", "logos" in html_content)
    print("CTA in html_content:", "cta-section" in html_content)
else:
    print("Body not found")
