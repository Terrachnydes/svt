# Synchro des sites SVT

Ce dossier sert à garder à jour les sites d'Erwan sur GitHub Pages
(`https://svt-prevert.github.io/svt/<fichier>`) et sa page récap
« Mes sites SVT » (https://claude.ai/artifact/BqXoxoAUJpBPUkC8mgAK3q).
Il commence par `_`, donc GitHub Pages ne le publie pas.

## Fichiers

- `sites.json` : la liste des sites.
  - `sites` : un site par entrée : `titre`, `theme` (une valeur de `themes`), `fichier` (nom du fichier à la racine du dépôt), `artifact` (lien Claude, ou `null` si le site n'existe que sur GitHub), `version` (dernière version de l'artifact copiée sur GitHub), `verifie` (date de la dernière vérification), `conversation` (facultatif : lien de la conversation Claude où le site se modifie ; sinon le bouton « Modifier avec Claude » ouvre l'artifact).
  - `ignores` : artifacts à ne jamais publier (documents Claude, outils privés, la page récap elle-même).
  - `en_attente` : nouveaux sites repérés, pas encore validés par Erwan.
- `build_hub.py` : refait les aperçus des fichiers donnés en argument et régénère `mes-sites.html`. Il lance aussi `sans_memoire.py` sur tous les sites.
- `sans_memoire.py` : ajoute en tête de chaque site un script qui vide `localStorage`/`sessionStorage` à chaque ouverture. Erwan ne veut **aucune mémoire** dans ses sites (sinon les réponses d'un élève restent pour le suivant, et une modification du site peut ne pas apparaître). Une page recopiée depuis son artifact le perd : `build_hub.py` le remet automatiquement. Ne jamais l'enlever.
- `tpl.html` : modèle de la page récap.
- `apercus/` : captures des sites (webp).

## Synchro automatique

Une tâche programmée (« Synchro sites SVT → GitHub ») tourne chaque nuit à minuit, heure de Paris.
Le bouton « Mettre à jour maintenant » de la page récap la lance aussi. Elle :

1. met à jour sur GitHub les sites déjà présents dans `sites.json` dont l'artifact a changé ;
2. ne publie JAMAIS un nouveau site seule : elle l'ajoute à `en_attente` ;
3. régénère les aperçus et la page récap, puis republie celle-ci.

## Ajouter un nouveau site (quand Erwan dit « mets ce site en ligne »)

Cette phrase veut dire : GitHub + page « Mes sites SVT » + colonne F du Google Sheet, les trois à la fois.

1. Copier la page HTML de l'artifact à la racine du dépôt, avec un nom sans espaces ni accents (ex. `phalene-bouleau.html`).
2. Ajouter l'entrée dans `sites.json` → `sites` (avec la `version` lue), et le retirer de `en_attente`.
3. `python3 _recap/build_hub.py <fichier>.html`, commit, push.
4. Lire puis republier la page récap avec `_recap/mes-sites.html`, sans passer `capabilities`.
5. Ajouter l'URL GitHub du site dans la « liste blanche » du cahier numérique : Google Sheet `1ABGFTjPtowzLW2vnhZ20Bmk63kC5lYjzouLHpYwfi30`, onglet `Cours`, colonne F, première case vide à partir de F100, F99 étant le titre « Liste blanche » (connecteur Google Sheets).

## Organisation des catégories

Le bouton « Organiser mes sites » de la page récap permet à Erwan de déplacer un site dans une autre catégorie (glisser-déposer ou menu « Catégorie »), de renommer, réordonner, créer ou supprimer (si vide) une catégorie.
C'est enregistré dans la base de la page (capacité `db`), document `organisation/config` :
`{"themes": [catégories dans l'ordre], "place": {fichier: catégorie}, "ren": {catégorie d'origine: nouveau nom}}`.
La page applique ce document par-dessus `sites.json` : c'est lui qui fait foi.

Pour recopier l'organisation dans `sites.json` (la synchro de nuit le fait) :
1. Lire le document : `ArtifactData`, action `get`, url de la page récap, collection `organisation`, doc_id `config`. S'il n'existe pas, il n'y a rien à faire.
2. L'enregistrer en JSON dans un fichier, puis `python3 _recap/apply_orga.py <fichier>.json`.
3. Si `sites.json` a changé : `python3 _recap/build_hub.py`, commit, push, republier la page récap.

Quand on ajoute un nouveau site, lui donner une catégorie qui existe déjà dans `sites.json` → `themes` (après la recopie ci-dessus).

## Consignes et correction

Chaque carte de la page récap a un bouton « Consignes » : nombre de consignes, niveau (6e → 2nde), difficulté, durée et précisions,
puis Claude génère les consignes et le barème sur 20 (capacité `sample` de la page, sur le compte de la personne qui l'utilise).
Le contenu du site envoyé à Claude est un extrait automatique des textes, boutons et réglages du fichier (`fiche()` dans `build_hub.py`).
## Onglet « Progression SVT »

La page a deux onglets : « Mes sites » et « Progression SVT » (adresse `#progression`).
L'onglet Progression lit le Google Sheet du cahier numérique (`1ABGFTjPtowzLW2vnhZ20Bmk63kC5lYjzouLHpYwfi30`, onglets `Cours`, `Consignes`, `Règles IA`, `Activités`) avec le connecteur Google Sheets.
Colonne « Lien » (sites hors activités, ex. orientation, visibles par tous les élèves) puis 3e / 4e / 5e / 6e, séances les unes sous les autres, 5 activités par séance (structure de l'onglet `Cours`).
Chaque carte : S{séance}.{n°} + titre, problématique (modifiables d'un clic), bouton « ✦ Consignes · Correction » (panneau Claude, capacité `sample`), site (Consulter / Modifier) ou « + Créer un site », flèche de publication.

Onglet `Activités` = brouillon + version publiée, une ligne par activité (`5e-S3-A2`), titre de séance (`5e-S3`) ou lien (`LIEN-…`) :
A clé · B type (activité / séance / lien) · C niveau · D séance · E n° · F-J brouillon (titre, problématique, consignes JSON, correction JSON, site) · K-O publié (mêmes champs) · P publié le · Q modifié le · R id du Doc activité.
Les 12 séances × 5 activités sont toujours affichées. Sans ligne, le brouillon d'une activité de la séance 3 reprend `Consignes` (site, consignes, correction) ; toutes les autres partent vierges (`SEANCES_REPRISES` dans tpl.html). Les titres de séance reprennent `Cours`. Flèche rouge = jamais publié (P vide), jaune = brouillon ≠ publié, verte = identiques.
Publier copie F-J dans K-O et ajoute l'adresse du site à la liste blanche (Cours!F100…) si elle manque.
Un site créé depuis « + Créer un site » se range en écrivant son adresse en colonne J de la ligne de la clé (et le titre en F pour un lien), jamais dans K-P.
Le cahier des élèves (dépôt cahier-numerique, `lirePublie_` dans Affichage.js) lit les colonnes K-P : une activité publiée remplace titre, problématique, consignes, site et correction des Docs ; la correction automatique utilise le barème publié (`baremePublieTexte_`) ; les liens publiés s'ajoutent aux liens de tous les niveaux. Envoi aux élèves par la synchro (toutes les 5 min).

La page déclare les capacités `mcp` (bouton de synchro : Claude Code Remote `fire_trigger` ; onglet Progression : Google Sheets `get_values`, `append_values`, `update_values`), `sample` (consignes et progression), `db` et `user` (organisation des catégories) : ne pas les retirer en republiant (republier SANS passer `capabilities` les conserve).

## Onglets « Suivi des élèves » et « Activité » (interface prof)

Adresses `#suivi` et `#activite`. Ils lisent un petit classeur à part, « Cahier numérique — interface prof »,
dont l'identifiant est dans le Sheet principal en `'Règles IA'!B5`. Il est rempli par Apps Script
(`src/InterfaceProf.js` du dépôt cahier-numerique) :
- `Suivi` : A type (classe / eleve / activite) · B classe · C clé · D données JSON · E mis à jour. Refait toutes les heures et après chaque commande.
- `Commandes` : la page y ajoute une ligne (A id · B date · C commande · D classe · E paramètres JSON · F « en attente »). La synchro des 5 min la traite : `ouvrir` / `fermer` / `facultative` / `arreter` (paramètre `ligne` = 1re ligne du bloc), `corriger`, `appreciations` (`periode`, `seulementClasse`), `actualiser`.
- `Connectés` : A1 = JSON (élèves vus ces 15 dernières min, créneaux du jour), toutes les 5 min en journée.
Écritures directes dans le Sheet principal : case Pronote d'un devoir (ligne 39/71/103) et appréciations (colonne AD).
Les noms des élèves viennent du fichier `eleves.csv` chargé dans la page (jamais envoyé à Google ; option « garder sur cet ordinateur »).
