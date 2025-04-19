#!/usr/bin/python3
"""
Markdown to HTML converter - Task 0 only
"""

import sys
import os

# Check number of arguments
if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if input file exists
if not os.path.isfile(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    sys.exit(1)

# Read input file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Write to output file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

sys.exit(0)
