# Tableau comparatif — Benchmark Mistral Assurances

> Document à remettre à **Inès Tabet** (responsable actuariat). Doit être
> lisible par un actuaire, pas par un data scientist.
> Auteur : `<prénom>` — Date : `<date>`

## Méthodologie

- **Split** : `<TimeSeriesSplit n_splits=5>` *(ou KFold n_splits=5, justifié dans le notebook)*
- **Métriques** : MAE, RMSE, R² (moyennes sur N folds)
- **Mêmes folds, mêmes features** pour tous les modèles (règle d'or *comparabilité*)
- **Hyperparamètres** : par défaut + 1 variante raisonnable par famille
- **Référence** : baseline `mistral-tarif-v1` (LinearRegression 2024)

## Tableau (à compléter)

| Modèle | MAE | RMSE | R² | Temps train (s) | Latence inférence (ms/1k) | Explicabilité (1-3) | Mémoire (Mo) |
|---|---|---|---|---|---|---|---|
| **mistral-tarif-v1** (baseline) | 105.0 | 139.4 | 0.39 | ~0.1 | ~1 | 3 (très explicable) | ~0.5 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Interprétation pour Inès

> 1-2 paragraphes en langage actuaire (pas data scientist).

...

## Recommandation

Voir `verdict.md` (5 lignes max).

---

*Document remis à Inès Tabet — `<date>`.*
