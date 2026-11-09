#!/usr/bin/env python3
"""Recopie dans sites.json l'organisation faite sur la page « Mes sites SVT ».

Usage : python3 _recap/apply_orga.py organisation.json
  organisation.json = le document organisation/config de la base de la page
  récap ({"themes": [...], "place": {fichier: catégorie}, "ren": {ancienne: nouvelle}}),
  lu avec ArtifactData. Écrit les catégories (ordre + nom) et la catégorie de
  chaque site dans _recap/sites.json. Affiche ce qui a changé.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "sites.json")


def main():
    o = json.load(open(sys.argv[1], encoding="utf-8"))
    if "data" in o and "themes" not in o:  # résultat brut d'ArtifactData
        o = o["data"]
    themes = [t.strip() for t in o.get("themes", []) if isinstance(t, str) and t.strip()]
    place, ren = o.get("place", {}) or {}, o.get("ren", {}) or {}
    cfg = json.load(open(P, encoding="utf-8"))
    avant = json.dumps(cfg, ensure_ascii=False, sort_keys=True)
    for s in cfg["sites"]:
        g = place.get(s["fichier"])
        if not g or g not in themes:
            g = ren.get(s["theme"], s["theme"])
        if g != s["theme"]:
            print(f"- {s['titre']} : {s['theme']} → {g}")
        s["theme"] = g
        if g not in themes:
            themes.append(g)
    if themes != cfg["themes"]:
        print("- catégories :", " | ".join(themes))
    cfg["themes"] = themes
    if json.dumps(cfg, ensure_ascii=False, sort_keys=True) == avant:
        print("aucun changement")
        return
    json.dump(cfg, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("sites.json mis à jour")


if __name__ == "__main__":
    main()
