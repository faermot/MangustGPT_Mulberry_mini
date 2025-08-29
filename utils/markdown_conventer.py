import re
from typing import List, Tuple


def _extract_links_with_placeholders(text: str) -> Tuple[str, List[Tuple[int,str,str]]]:
    links, out, last, i, idx, n = [], [], 0, 0, 0, len(text)
    while i < n:
        if text[i] == '[':
            j = text.find(']', i + 1)
            if j == -1:
                i += 1; continue
            label, k = text[i+1:j], j+1
            while k < n and text[k].isspace(): k += 1
            if k < n and text[k] == '(':
                depth, m = 0, k+1
                while m < n:
                    if text[m] == '(': depth += 1
                    elif text[m] == ')':
                        if depth == 0:
                            out.append(text[last:i])
                            placeholder = f'@@LINK{idx}@@'
                            out.append(placeholder)
                            links.append((idx, label, text[k+1:m]))
                            idx, last, i = idx+1, m+1, m+1
                            break
                        depth -= 1
                    m += 1
                else: i += 1; continue
                continue
        i += 1
    out.append(text[last:])
    return ''.join(out), links


def convert_to_telegram_md_v2(text: str) -> str:
    def make_replacer(store, tag, wrap=None):
        def _repl(m):
            content = m.group(1).strip()
            placeholder = f'@@{tag}{len(store)}@@'
            store.append((placeholder, content if wrap is None else wrap(content)))
            return placeholder
        return _repl

    code_blocks = []
    text = re.sub(
        r'```([^\n`]*)\n(.*?)```',
        lambda m: (code_blocks.append(
            (ph := f'@@CODEBLOCK{len(code_blocks)}@@', m.group(1).strip(), m.group(2))) or ph),
        text, flags=re.DOTALL
    )

    inline_codes = []
    text = re.sub(r'`([^`\n]+?)`',
        lambda m: (inline_codes.append((ph := f'@@INLINE{len(inline_codes)}@@', m.group(1))) or ph),
        text
    )

    text, links = _extract_links_with_placeholders(text)

    headings = []
    text = re.sub(r'(?m)^\s{0,3}#{1,6}\s+(.*)$', make_replacer(headings, 'HEADING'), text)

    bold_chunks, italic_chunks = [], []
    text = re.sub(r'\*\*(.+?)\*\*|__(.+?)__', make_replacer(bold_chunks, 'BOLD'), text)
    text = re.sub(r'(?<!\S)\*(?!\s)(.+?)(?<!\s)\*(?!\S)|_(.+?)_', make_replacer(italic_chunks, 'ITAL'), text)

    def esc(s): return re.sub(r'([_\*\[\]\(\)~`>#+=\-\|{}\.\!\\])', r'\\\1', s)
    text = esc(text)

    for ph, c in bold_chunks:   text = text.replace(ph, f'*{esc(c)}*')
    for ph, c in italic_chunks: text = text.replace(ph, f'_{esc(c)}_')
    for ph, c in headings:      text = text.replace(ph, f'*{esc(c)}*')
    for idx, label, url in links: text = text.replace(f'@@LINK{idx}@@', f'[{esc(label)}]({url})')
    for ph, c in inline_codes:  text = text.replace(ph, f'`{c}`')
    for ph, lang, c in code_blocks:
        text = text.replace(ph, f'```{lang}\n{c}\n```' if lang else f'```\n{c}\n```')

    return text
