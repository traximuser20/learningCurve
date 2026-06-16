import html.parser

class TagChecker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        if tag not in ['img', 'br', 'hr', 'link', 'meta', 'input', 'col', 'base', 'area']:
            self.stack.append((tag, self.getpos()))
    
    def handle_endtag(self, tag):
        if tag in ['img', 'br', 'hr', 'link', 'meta', 'input', 'col', 'base', 'area']:
            return
        if not self.stack:
            self.errors.append(f"Unmatched closing tag </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tags: <{last_tag}> from line {pos[0]} closed by </{tag}> at line {self.getpos()[0]}")

with open('src/ClaudeCode.html', 'r') as f:
    content = f.read()

checker = TagChecker()
checker.feed(content)
for error in checker.errors:
    print(error)
if checker.stack:
    for tag, pos in checker.stack:
        print(f"Unclosed tag <{tag}> from line {pos[0]}")
