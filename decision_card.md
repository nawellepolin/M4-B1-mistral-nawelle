# Carte de décision personnelle — M4-B1

> **Ton ébauche perso** de la grille de décision C4, **avant** la
> restitution collective de mercredi. À confronter aux propositions des
> autres pour construire la grille commune.
> Auteur : `<prénom>` — Date : `<date>`

## Critères que je mobilise (mon ordre de priorité)

1. ... (ex. *« Précision sur le pic printemps-été »*)
2. ...
3. ...
4. ...

## Modèles que j'ai benchmarkés

> Liste rapide.

- Famille A : ...
- Famille B : ...
- Famille C : ...

## Pour quel cas je choisirais chaque famille ?

> Si Inès me demandait *« et pour un cas X, vous prendriez quoi ? »*.

| Cas | Famille recommandée | Pourquoi |
|---|---|---|
| **Mistral Bike Sharing (saisonnalité forte)** | ... | ... |
| **Cas similaire mais 100 lignes seulement** | ... | ... |
| **Cas avec exigence d'explicabilité réglementaire** | ... | ... |
| **Cas avec latence < 5 ms imposée** | ... | ... |

## Analyse éthique et réglementaire (C2)

> ~5 lignes. Le geste : **évaluer s'il existe réellement des risques**, puis
> **conclure**. Conclure « risque faible » est une réponse valide et
> professionnelle — pas besoin d'inventer un problème.

- Le dataset contient-il des **données personnelles** ? ...
- Utilise-t-on un **attribut sensible** / y a-t-il un risque de **biais** envers une population ? ...
- Y a-t-il un enjeu **RGPD / confidentialité** ? ...
- Quel **impact sociétal** de l'usage du modèle (destinataires directs/indirects) ? ...
- **Conclusion** : ... (ex. *« données agrégées, pas de PII → risque faible ;
  si on exploitait des trajets individuels, il faudrait une analyse RGPD +
  minimisation + réidentification »*)

## Ouverture — Robustesse d'une solution d'IA (hors C2, prépare M7)

> Cette activité **ne relève pas de C2**. C'est un **complément à ta décision
> C4** et une ouverture vers **M7** (menaces sur les systèmes d'IA) : un réflexe
> pro = évaluer les limites d'un modèle au-delà de ses performances. Une ligne
> suffit. Cf. mini-cours `06_Menaces_robustesse_essentiel.md`.

- **Vulnérabilité identifiée** : ... (ex. extrapole sans alerter sur une
  température hors-distribution)
- **Garde-fou envisagé** en conception : ... (ex. contrôle des bornes d'entrée /
  seuil d'abstention) — *mitigation complète = M7, monitoring du drift = M6*

## Ce que je veux apporter à la grille collective

> 1-2 contributions ou questions à pousser pendant la restitution.

- ...
- ...

---

*Carte personnelle à compléter avant la restitution collective mercredi 11h30.*
