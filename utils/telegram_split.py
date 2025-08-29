import re


def split_message(text, limit=4096):
    parts = []
    buf = ""
    open_code = False
    code_lang = ""

    lines = text.split("\n")

    for line in lines:
        if line.startswith("```") and not open_code:
            open_code = True
            code_lang = line[3:].strip()
        elif line.startswith("```") and open_code:
            open_code = False
            code_lang = ""

        line_to_add = line + "\n"

        if len(buf) + len(line_to_add) > limit:
            if open_code:
                buf += line_to_add
                continue
            else:
                parts.append(buf)
                buf = line_to_add
        else:
            buf += line_to_add

    if buf:
        parts.append(buf)

    return parts
