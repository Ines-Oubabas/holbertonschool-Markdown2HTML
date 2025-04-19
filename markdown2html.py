#!/usr/bin/python3
"""
Markdown to HTML converter - Task 0 only
"""

import sys
import os

# Vérifier le nombre d'arguments
if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Vérifier si le fichier markdown d'entrée existe
if not os.path.isfile(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    sys.exit(1)

# Lecture et écriture
with open(input_file, 'r') as f_in:
    content = f_in.read()

with open(output_file, 'w') as f_out:
    f_out.write(content)

# Sortie silencieuse
sys.exit(0)
