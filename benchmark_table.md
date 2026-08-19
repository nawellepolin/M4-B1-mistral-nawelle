# Tableau comparatif — Benchmark Mistral Assurances

> Document à remettre à **Inès Tabet** (responsable actuariat). Doit être
> lisible par un actuaire, pas par un data scientist.
> Auteur : `Nawelle` — Date : `2026-08-19`

## Méthodologie

- **Split** : `TimeSeriesSplit n_splits=5` — les données sont chronologiques
  (2011→2012), donc on entraîne toujours sur le passé et on teste sur la
  période qui suit (pas de `KFold` classique, qui mélangerait passé et
  futur).
- **Métriques** : MAE, RMSE, R² (moyennes sur les 5 morceaux)
- **Mêmes folds, mêmes features** pour tous les modèles (règle d'or *comparabilité*)
- **Hyperparamètres** : réglages par défaut (RandomForest : profondeur
  limitée à 18 pour éviter un fichier disproportionné, cf. `decision_card.md`)
- **Référence** : baseline `mistral-tarif-v1` (LinearRegression 2024)

## Tableau (à compléter)

| Modèle | MAE | RMSE | R² | Temps train (s) | Latence inférence (ms/1k) | Explicabilité (1-3) | Mémoire (Mo) |
|---|---|---|---|---|---|---|---|
| **mistral-tarif-v1** (baseline) | 105.0 | 139.4 | 0.39 | ~0.1 | ~1 | 3 (très explicable) | ~0.5 |
| **HistGradientBoosting** | 51.5 | 75.2 | 0.80 | 0.33 | 2.4 | 1 (peu explicable) | ~0.4 |
| **RandomForest** | 53.7 | 81.0 | 0.77 | 0.41 | 13.6 | 2 (moyennement explicable) | ~82 |
| **Ridge** (linéaire) | 103.7 | 142.1 | 0.37 | 0.004 | 1.9 | 3 (très explicable) | < 0.1 |

## Interprétation pour Inès

Le modèle actuel (`mistral-tarif-v1`) se trompe en moyenne de 105 trajets
par heure prédite. En testant d'autres approches sur les mêmes données et
les mêmes périodes de test, on trouve un modèle (HistGradientBoosting) qui
divise cette erreur par deux : environ 51 trajets d'écart en moyenne, contre
105 aujourd'hui. Il explique aussi beaucoup mieux les variations observées
(80 % contre 39 % aujourd'hui).

Le compromis : ce modèle est une "boîte noire" plus difficile à justifier
en détail (contrairement au modèle actuel, où on peut lire l'effet de
chaque facteur). Un autre candidat (RandomForest) offre une précision
presque aussi bonne, un peu plus lisible, mais produit un fichier
~160 fois plus lourd (82 Mo contre 0.4 Mo) sans réel gain en échange. La
version linéaire améliorée (Ridge) reste, elle, aussi facile à justifier
que le modèle actuel, mais n'apporte quasiment aucun gain de précision.

## Recommandation

Voir `verdict.md` (5 lignes max).

---

*Document remis à Inès Tabet — `2026-08-19`.*
