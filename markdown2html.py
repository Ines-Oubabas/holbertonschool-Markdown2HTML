#!/usr/bin/python3
"""
Markdown to HTML converter
"""

import sys
import os
import hashlib
import re


def convert_md5(line):
    """Convert [[content]] to MD5 hash"""
    return re.sub(r'\[\[(.*?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)


def convert_remove_c(line):
    """Remove 'c' and 'C' from ((content))"""
    return re.sub(r'\(\((.*?)\)\)', lambda m: re.sub(r'[cC]', '', m.group(1)), line)


def convert_bold_emphasis(line):
    """Convert bold and emphasis markdown to HTML"""
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    return line


def parse_line(line):
    """Parse line for markdown transformations"""
    line = convert_md5(line)
    line = convert_remove_c(line)
    line = convert_bold_emphasis(line)
    return line


def markdown_to_html(input_file, output_file):
    """Convert Markdown to HTML"""

    with open(input_file, 'r') as md, open(output_file, 'w') as html:
        ul_open = False
        ol_open = False
        paragraph = []

        for line in md:
            stripped = line.strip()

            if not stripped:
                if paragraph:
                    html.write("<p>\n" + "<br/>\n".join(parse_line(p) for p in paragraph) + "\n</p>\n")
                    paragraph = []
                if ul_open:
                    html.write("</ul>\n")
                    ul_open = False
                if ol_open:
                    html.write("</ol>\n")
                    ol_open = False
                continue

            if re.match(r'^#{1,6} ', stripped):
                if paragraph:
                    html.write("<p>\n" + "<br/>\n".join(parse_line(p) for p in paragraph) + "\n</p>\n")
                    paragraph = []
                if ul_open:
                    html.write("</ul>\n")
                    ul_open = False
                if ol_open:
                    html.write("</ol>\n")
                    ol_open = False
                level = len(stripped.split(' ')[0])
                content = ' '.join(stripped.split(' ')[1:])
                html.write(f"<h{level}>{parse_line(content)}</h{level}>\n")

            elif stripped.startswith('- '):
                if ol_open:
                    html.write("</ol>\n")
                    ol_open = False
                if not ul_open:
                    html.write("<ul>\n")
                    ul_open = True
                html.write(f"<li>{parse_line(stripped[2:])}</li>\n")

            elif stripped.startswith('* '):
                if ul_open:
                    html.write("</ul>\n")
                    ul_open = False
                if not ol_open:
                    html.write("<ol>\n")
                    ol_open = True
                html.write(f"<li>{parse_line(stripped[2:])}</li>\n")

            else:
                paragraph.append(stripped)

        # Close any open tags at the end
        if paragraph:
            html.write("<p>\n" + "<br/>\n".join(parse_line(p) for p in paragraph) + "\n</p>\n")
        if ul_open:
            html.write("</ul>\n")
        if ol_open:
            html.write("</ol>\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"Missing {input_path}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_path, output_path)
    sys.exit(0)
