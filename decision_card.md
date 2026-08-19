# Carte de décision personnelle — M4-B1

> **Ton ébauche perso** de la grille de décision C4, **avant** la
> restitution collective de mercredi. À confronter aux propositions des
> autres pour construire la grille commune.
> Auteur : `Nawelle` — Date : `2026-08-19`

## Critères que je mobilise (mon ordre de priorité)

1. **La précision au printemps/été** — c'est la période où il y a le plus de
   trajets, donc une erreur là coûte le plus cher.
2. **Pouvoir expliquer le résultat** — avec l'assurance, on doit pouvoir
   justifier un tarif, pas juste se baser sur le modèle.
3. **Marcher même avec peu de données** — un modèle utile même sur un petit
   historique (nouvelle ville) vaut mieux qu'un modèle qui a besoin de
   beaucoup de données pour être bon.
4. **Le coût (vitesse + mémoire)** — seulement si les 3 points au-dessus sont
   à peu près égaux entre deux modèles.

## Modèles que j'ai benchmarkés

> Liste rapide (3 familles, même découpage `TimeSeriesSplit` à 5 morceaux,
> mêmes colonnes en entrée).

- Famille A : **Ridge** (régression linéaire) — `hour`/`month` transformées
  en sin/cos, données mises à l'échelle avec `StandardScaler`.
- Famille B : **RandomForest** — profondeur limitée à 18 (`max_depth=18`) et
  au moins 3 exemples par feuille (`min_samples_leaf=3`). Sans cette limite,
  chaque arbre pousse jusqu'à coller aux 17 000 lignes d'entraînement (donc
  au bruit, pas juste au signal utile) : ça donne un fichier `.joblib`
  d'environ 300 Mo pour un R² à peine meilleur. Limiter la profondeur, c'est
  perdre un tout petit peu de précision pour gagner beaucoup en taille de
  fichier et en généralisation.
- Famille C : **HistGradientBoosting** — réglages par défaut.

Résultats obtenus (moyenne sur les 5 morceaux) :

| Modèle | MAE (erreur moyenne) | RMSE | R² (0 à 1, + haut = mieux) | Taille du fichier |
|---|---|---|---|---|
| HistGradientBoosting | 51.5 | 75.2 | 0.80 | ~0.4 Mo |
| RandomForest | 53.7 | 81.0 | 0.77 | ~82 Mo |
| Ridge (linéaire) | 103.7 | 142.1 | 0.37 | < 0.1 Mo |
| *baseline v1 (ancien modèle 2024)* | *105.0* | *139.4* | *0.39* | *~0.5 Mo* |

→ Ça confirme ce que le notebook prévoyait : HistGradientBoosting gagne
nettement. Son MAE (51.5) veut dire qu'il se trompe en moyenne de ~51 trajets,
contre ~104 pour Ridge — deux fois moins d'erreur. Son R² de 0.80 (contre 0.37
pour Ridge) veut dire qu'il explique 80 % de la variation du nombre de
trajets, contre 37 % seulement pour Ridge — la relation entre les variables
et le nombre de trajets n'est pas une simple ligne droite.

## Pour quel cas je choisirais chaque famille ?

> Si Inès me demandait *« et pour un cas X, vous prendriez quoi ? »*.

| Cas | Famille recommandée | Pourquoi |
|---|---|---|
| **Mistral Bike Sharing (saisonnalité forte)** | HistGradientBoosting | C'est le modèle qui se trompe le moins en moyenne (MAE le plus bas) et le moins fort sur ses pires cas (RMSE le plus bas), et qui explique le plus de la variation observée (R² le plus haut) — tout en restant rapide. |
| **Cas similaire mais 100 lignes seulement** | Ridge (linéaire) | RandomForest et HistGradientBoosting ont besoin de beaucoup de données pour bien apprendre ; avec seulement 100 lignes ils risquent d'apprendre "par cœur" au lieu de généraliser. Un modèle plus simple comme Ridge tient mieux. |
| **Cas avec obligation d'expliquer le résultat** | Ridge (linéaire) | On peut lire directement l'effet de chaque variable dans ses coefficients. Pour les deux autres, il faut des outils en plus pour expliquer pourquoi le modèle a prédit tel chiffre. |
| **Cas avec une réponse imposée en moins de 5 ms** | HistGradientBoosting (ou Ridge) | Les deux répondent largement à temps (2.4 ms et 1.9 ms pour 1000 prédictions). RandomForest est à éviter ici, il est 7 fois plus lent (13.6 ms). |

## Analyse éthique et réglementaire (C2)

> ~5 lignes. Le geste : **évaluer s'il existe réellement des risques**, puis
> **conclure**. Conclure « risque faible » est une réponse valide et
> professionnelle — pas besoin d'inventer un problème.

- Le dataset contient-il des **données personnelles** ? Non — ce sont des
  comptages par heure (combien de trajets), pas les trajets d'une personne
  identifiable.
- Utilise-t-on un **attribut sensible** / y a-t-il un risque de **biais** envers une population ? Les colonnes utilisées sont la météo et le calendrier — pas d'âge, de genre, de zone géographique ou autre info sensible.
- Y a-t-il un enjeu **RGPD / confidentialité** ? Non pour l'instant, vu que les données sont déjà agrégées. Il faudrait revérifier si un jour on ajoute des données de trajets individuels.
- Quel **impact sociétal** de l'usage du modèle (destinataires directs/indirects) ? Impact limité — le modèle sert à estimer un volume global, pas à prendre une décision sur une personne précise.
- **Conclusion** : données agrégées, pas d'info personnelle, pas d'attribut sensible → **risque faible**. À revoir seulement si le périmètre change (données individuelles).

## Ouverture — Robustesse d'une solution d'IA (hors C2, prépare M7)

> Cette activité **ne relève pas de C2**. C'est un **complément à ta décision
> C4** et une ouverture vers **M7** (menaces sur les systèmes d'IA) : un réflexe
> pro = évaluer les limites d'un modèle au-delà de ses performances. Une ligne
> suffit. Cf. mini-cours `06_Menaces_robustesse_essentiel.md`.

- **Vulnérabilité identifiée** : face à une valeur jamais vue à l'entraînement
  (météo extrême par exemple), RandomForest et HistGradientBoosting ne
  peuvent pas vraiment "deviner au-delà" — ils donnent quand même une
  réponse, sans prévenir qu'ils sortent de leur zone de confiance.
- **Garde-fou envisagé** en conception : vérifier que chaque donnée reçue
  reste dans la plage vue pendant l'entraînement, et alerter/refuser sinon

## Ce que je veux apporter à la grille collective

> 1-2 contributions ou questions à pousser pendant la restitution.

- Faut-il quand même privilégier un modèle plus simple à expliquer, même
  quand la loi ne l'exige pas pour ce cas précis ?
- Comment choisir entre "le modèle qui se trompe le moins" (HistGradientBoosting) et "le modèle qui prend le moins de place" (RandomForest fait 82 Mo, 200x plus gros) quand ce n'est pas embarqué sur un petit appareil ?

---

*Carte personnelle à compléter avant la restitution collective mercredi 11h30.*
