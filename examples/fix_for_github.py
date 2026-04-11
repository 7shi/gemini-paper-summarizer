import re, sys

def add_display_math_spacing(text):
    # A line consisting entirely of a math expression should be rendered as
    # display math. Convert $...$ to $$...$$ and, for non-indented lines,
    # ensure blank lines before and after so GitHub renders it as a block.
    # Indented lines (e.g. inside a list) are converted to $$...$$ without
    # adding blank lines, which would break list formatting.
    lines = text.splitlines()
    result = []
    for i, line in enumerate(lines):
        s = line.strip()
        is_solo = s.startswith('$') and s.endswith('$')
        if is_solo:
            is_indented = line[0].isspace()
            if s.startswith('$') and not s.startswith('$$'):
                # Preserve leading whitespace; use lstrip to avoid counting
                # trailing spaces as part of the indent.
                indent = line[:len(line) - len(line.lstrip())]
                line = indent + '$$' + s[1:-1] + '$$'
            if not is_indented:
                if result and result[-1].strip():
                    result.append('')
            result.append(line)
            if not is_indented:
                if i + 1 < len(lines) and lines[i + 1].strip():
                    result.append('')
        else:
            result.append(line)
    return '\n'.join(result) + '\n'

def fix_math_underscores(text):
    # GitHub's Markdown parser interprets \_ as an escaped underscore before
    # passing content to the math renderer, so \_ inside $...$ must be written
    # as \\_ to produce the intended LaTeX \_ (literal underscore).
    def fix_block(m):
        return re.sub(r'(?<!\\)\\_', r'\\\\_', m.group(0))
    text = re.sub(r'\$\$.+?\$\$', fix_block, text, flags=re.DOTALL)
    text = re.sub(r'\$[^\n$]+?\$', fix_block, text)
    return text

for path in sys.argv[1:]:
    with open(path, encoding='utf-8') as f:
        original = f.read()
    fixed = add_display_math_spacing(fix_math_underscores(original))
    if fixed != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f"Fixed: {path}")
