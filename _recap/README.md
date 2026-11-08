# Synchro des sites SVT

Ce dossier sert à garder à jour les sites d'Erwan sur GitHub Pages
(`https://terrachnydes.github.io/svt/<fichier>`) et sa page récap
« Mes sites SVT » (https://claude.ai/artifact/BqXoxoAUJpBPUkC8mgAK3q).
Il commence par `_`, donc GitHub Pages ne le publie pas.

## Fichiers

- `sites.json` : la liste des sites.
  - `sites` : un site par entrée : `titre`, `theme` (une valeur de `themes`), `fichier` (nom du fichier à la racine du dépôt), `artifact` (lien Claude, ou `null` si le site n'existe que sur GitHub), `version` (dernière version de l'artifact copiée sur GitHub), `verifie` (date de la dernière vérification).
  - `ignores` : artifacts à ne jamais publier (documents Claude, outils privés, la page récap elle-même).
  - `en_attente` : nouveaux sites repérés, pas encore validés par Erwan.
- `build_hub.py` : refait les aperçus des fichiers donnés en argument et régénère `mes-sites.html`.
- `tpl.html` : modèle de la page récap.
- `apercus/` : captures des sites (webp).

## Synchro automatique

Une tâche programmée (« Synchro sites SVT → GitHub ») tourne chaque nuit à minuit, heure de Paris.
Le bouton « Mettre à jour maintenant » de la page récap la lance aussi. Elle :

1. met à jour sur GitHub les sites déjà présents dans `sites.json` dont l'artifact a changé ;
2. ne publie JAMAIS un nouveau site seule : elle l'ajoute à `en_attente` ;
3. régénère les aperçus et la page récap, puis republie celle-ci.

## Ajouter un nouveau site (quand Erwan le demande)

1. Copier la page HTML de l'artifact à la racine du dépôt, avec un nom sans espaces ni accents (ex. `phalene-bouleau.html`).
2. Ajouter l'entrée dans `sites.json` → `sites` (avec la `version` lue), et le retirer de `en_attente`.
3. `python3 _recap/build_hub.py <fichier>.html`, commit, push.
4. Lire puis republier la page récap avec `_recap/mes-sites.html`, sans passer `capabilities`.
5. Ajouter l'URL GitHub du site dans la « liste blanche » du cahier numérique : Google Sheet `1ABGFTjPtowzLW2vnhZ20Bmk63kC5lYjzouLHpYwfi30`, onglet `Cours`, colonne F, première case vide à partir de F100 (connecteur Google Sheets).
