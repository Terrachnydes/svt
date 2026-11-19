#!/usr/bin/env python3
"""Empêche les sites de garder en mémoire les réponses des élèves.

Ajoute en tête de chaque page un petit script qui vide localStorage et
sessionStorage à chaque ouverture : le site repart toujours de zéro.
Sans risque si on le relance (le script n'est ajouté qu'une fois).

Usage : python3 _recap/sans_memoire.py            -> tous les sites de sites.json
        python3 _recap/sans_memoire.py a.html ... -> seulement ces fichiers
"""
import json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- sans-memoire -->"
SNIP = (MARK + "<script>/* Aucune memoire : le site repart de zero a chaque ouverture */"
        "try{localStorage.clear();sessionStorage.clear()}catch(e){}</script>")


def traite(chemin):
    s = open(chemin, encoding="utf-8").read()
    if MARK in s:
        return "déjà fait"
    m = re.search(r"<head[^>]*>", s, re.I)
    if m:
        s = s[:m.end()] + "\n" + SNIP + s[m.end():]
    else:
        m = re.search(r"<!doctype[^>]*>", s, re.I)
        pos = m.end() if m else 0
        s = s[:pos] + "\n" + SNIP + "\n" + s[pos:]
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
            print(f"{traite(p)} : {f}")
        else:
            print(f"introuvable : {f}")


if __name__ == "__main__":
    main()
