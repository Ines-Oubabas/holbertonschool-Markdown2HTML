#!/usr/bin/python3
"""
Markdown to HTML converter - Task 0 only
"""

import sys
import os

if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    sys.exit(1)

# Copier le contenu du fichier markdown dans le fichier HTML
with open(input_file, 'r', encoding='utf-8') as f_in:
    content = f_in.read()

with open(output_file, 'w', encoding='utf-8') as f_out:
    f_out.write(content)

sys.exit(0)
