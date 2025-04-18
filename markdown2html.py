#!/usr/bin/python3
"""
Simple Markdown to HTML converter - Task 0
"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        print(f"Missing {input_path}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)
