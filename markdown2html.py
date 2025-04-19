#!/usr/bin/python3
"""
Markdown to HTML converter - Tasks 0 to 3
"""

import os
import sys
import re

# Vérification des arguments
if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

fichier_markdown = sys.argv[1]
fichier_sortie = sys.argv[2]

if not os.path.exists(fichier_markdown):
    print(f"Missing {fichier_markdown}", file=sys.stderr)
    sys.exit(1)

# Lire le fichier Markdown
try:
    with open(fichier_markdown, 'r', encoding='utf-8') as f:
        contenu_markdown = f.read()
except UnicodeDecodeError:
    try:
        with open(fichier_markdown, 'r', encoding='ISO-8859-1') as f:
            contenu_markdown = f.read()
    except UnicodeDecodeError as e:
        print(f"Erreur de décodage dans {fichier_markdown}: {e}", file=sys.stderr)
        sys.exit(1)

# Fonctions de transformation
def convertir_titres(contenu):
    contenu = re.sub(r"###### (.*)", r"<h6>\1</h6>", contenu)
    contenu = re.sub(r"##### (.*)", r"<h5>\1</h5>", contenu)
    contenu = re.sub(r"#### (.*)", r"<h4>\1</h4>", contenu)
    contenu = re.sub(r"### (.*)", r"<h3>\1</h3>", contenu)
    contenu = re.sub(r"## (.*)", r"<h2>\1</h2>", contenu)
    contenu = re.sub(r"# (.*)", r"<h1>\1</h1>", contenu)
    return contenu

def convertir_listes(contenu):
    lignes = contenu.split('\n')
    nouveau_contenu = []
    dans_ul = False
    dans_ol = False

    for ligne in lignes:
        if re.match(r"^\s*- (.*)", ligne):  # Liste non ordonnée
            if not dans_ul:
                nouveau_contenu.append("<ul>")
                dans_ul = True
            texte = re.sub(r"^\s*- ", "", ligne)
            nouveau_contenu.append(f"<li>{texte}</li>")
        elif re.match(r"^\s*\* (.*)", ligne):  # Liste ordonnée
            if not dans_ol:
                nouveau_contenu.append("<ol>")
                dans_ol = True
            texte = re.sub(r"^\s*\* ", "", ligne)
            nouveau_contenu.append(f"<li>{texte}</li>")
        else:
            if dans_ul:
                nouveau_contenu.append("</ul>")
                dans_ul = False
            if dans_ol:
                nouveau_contenu.append("</ol>")
                dans_ol = False
            nouveau_contenu.append(ligne)

    if dans_ul:
        nouveau_contenu.append("</ul>")
    if dans_ol:
        nouveau_contenu.append("</ol>")

    return '\n'.join(nouveau_contenu)

def convertir_paragraphes(contenu):
    lignes = contenu.split('\n')
    result = []
    bloc = []

    for ligne in lignes:
        if ligne.strip() == "":
            if bloc:
                result.append("<p>\n" + "<br/>\n".join(bloc) + "\n</p>")
                bloc = []
        elif not re.match(r"<h[1-6]>|<ul>|<ol>|</ul>|</ol>|<li>|</li>", ligne.strip()):
            bloc.append(ligne.strip())
        else:
            if bloc:
                result.append("<p>\n" + "<br/>\n".join(bloc) + "\n</p>")
                bloc = []
            result.append(ligne)

    if bloc:
        result.append("<p>\n" + "<br/>\n".join(bloc) + "\n</p>")

    return '\n'.join(result)

# Traitement
contenu_html = contenu_markdown
contenu_html = convertir_titres(contenu_html)
contenu_html = convertir_listes(contenu_html)
contenu_html = convertir_paragraphes(contenu_html)

# Écriture dans le fichier de sortie
with open(fichier_sortie, 'w', encoding='utf-8') as f:
    f.write(contenu_html)

sys.exit(0)
