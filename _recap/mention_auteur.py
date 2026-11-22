#!/usr/bin/env python3
"""Ajoute la mention d'auteur sur chaque site.

- dans le code : un commentaire et <meta name="author"> en tête de page ;
- à l'écran : une petite ligne en bas de page.
Sans risque si on le relance (la mention n'est ajoutée qu'une fois).
Appelé automatiquement par build_hub.py, donc aussi par la synchro.

Usage : python3 _recap/mention_auteur.py            -> tous les sites de sites.json
        python3 _recap/mention_auteur.py a.html ... -> seulement ces fichiers
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- mention-auteur -->"
TEXTE = "© M. Gavens, professeur de SVT — Tous droits réservés. Reproduction interdite sans autorisation."
TETE = (MARK + "\n<!-- " + TEXTE + " -->\n"
        '<meta name="author" content="M. Gavens, professeur de SVT">\n'
        '<meta name="copyright" content="© M. Gavens — Tous droits réservés">')
# <div> (pas <footer>) pour ne pas hériter des styles « footer » propres à certains sites ;
# order/flex-shrink : reste en dernier et entier dans les pages en flex plein écran.
PIED = ('<div data-mention-auteur style="all:initial;display:block;box-sizing:border-box;'
        'order:9999;flex:0 0 auto;width:100%;max-width:1240px;margin:8px auto 4px;padding:4px 12px;text-align:center;'
        'font:12px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#6b7280;'
        'overflow-wrap:anywhere">' + TEXTE + "</div>")


def traite(chemin):
    s = open(chemin, encoding="utf-8").read()
    if MARK in s:
        return "déjà fait"
    m = re.search(r"<head[^>]*>", s, re.I)
    if m:
        s = s[:m.end()] + "\n" + TETE + s[m.end():]
    else:
        m = re.search(r"<!doctype[^>]*>", s, re.I)
        pos = m.end() if m else 0
        s = s[:pos] + "\n" + TETE + "\n" + s[pos:]
    fins = [x.start() for x in re.finditer(r"</body\s*>", s, re.I)]
    if fins:
        s = s[:fins[-1]] + PIED + "\n" + s[fins[-1]:]
    else:
        s = s.rstrip() + "\n" + PIED + "\n"
    open(chemin, "w", encoding="utf-8").write(s)
    return "ajouté"


def main():
    fichiers = sys.argv[1:]
    if not fichiers:
        d = json.load(open(os.path.join(REPO, "_recap", "sites.json"), encoding="utf-8"))
        fichiers = [x["fichier"] for x in d["sites"]]
    for f in fichiers:
        p = f if os.path.isabs(f) else os.path.join(REPO, f)
        if os.path.exists(p):
            print(traite(p), ":", f)
        else:
            print("introuvable :", f)


if __name__ == "__main__":
    main()
