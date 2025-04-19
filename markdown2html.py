#!/usr/bin/python3
"""
Markdown to HTML converter - Full version (Headings, Lists, Paragraphs, Bold, Emphasis, MD5, Remove 'c')
"""

import sys
import os
import re
import hashlib


def convert_headings(line):
    if line.startswith('#'):
        count = 0
        while count < len(line) and line[count] == '#':
            count += 1
        if 1 <= count <= 6 and len(line) > count and line[count] == ' ':
            content = line[count + 1:].strip()
            return f"<h{count}>{apply_inline_formatting(content)}</h{count}>"
    return None


def apply_inline_formatting(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    text = re.sub(r'\[\[(.+?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), text)
    text = re.sub(r'\(\((.+?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(1)), text)
    return text


def flush_paragraph(buffer, html_file):
    if buffer:
        html_file.write("<p>\n")
        html_file.write("<br/>\n".join(buffer) + "\n")
        html_file.write("</p>\n")
        buffer.clear()


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        paragraph_buffer = []
        in_ul = False
        in_ol = False

        for line in md_file:
            stripped = line.strip()

            if not stripped:
                flush_paragraph(paragraph_buffer, html_file)
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                continue

            heading = convert_headings(stripped)
            if heading:
                flush_paragraph(paragraph_buffer, html_file)
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                html_file.write(heading + '\n')
            elif stripped.startswith('- '):
                flush_paragraph(paragraph_buffer, html_file)
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                if not in_ul:
                    html_file.write("<ul>\n")
                    in_ul = True
                content = apply_inline_formatting(stripped[2:].strip())
                html_file.write(f"<li>{content}</li>\n")
            elif stripped.startswith('* '):
                flush_paragraph(paragraph_buffer, html_file)
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if not in_ol:
                    html_file.write("<ol>\n")
                    in_ol = True
                content = apply_inline_formatting(stripped[2:].strip())
                html_file.write(f"<li>{content}</li>\n")
            else:
                paragraph_buffer.append(apply_inline_formatting(stripped))

        flush_paragraph(paragraph_buffer, html_file)
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
