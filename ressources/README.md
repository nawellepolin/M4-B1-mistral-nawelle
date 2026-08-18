# Ressources M4-B1 — Index des mini-cours

> Brief associé : **M4-B1** (benchmark tabulaire Mistral Assurances, individuel).
> 🧭 **Le pilotage du brief (quoi faire, quand, avec quel appui) est dans le
> [`README.md`](../README.md) à la racine du repo** — ici, uniquement l'index
> des mini-cours.

| # | Mini-cours | En une ligne |
|---|---|---|
| 01 | [`01_EDA_saisonnalite_essentiel.md`](./01_EDA_saisonnalite_essentiel.md) | Visualiser la saisonnalité (saison, heure, météo) et en tirer des hypothèses de modèles |
| 02 | [`02_Split_temporel_vs_stratifie_essentiel.md`](./02_Split_temporel_vs_stratifie_essentiel.md) | Quand `TimeSeriesSplit`, quand `KFold` — anti-fuite temporelle |
| 03 | [`03_Metriques_regression_essentiel.md`](./03_Metriques_regression_essentiel.md) | MAE, RMSE, R² : lesquelles pour Mistral, et comment les lire |
| 04 | [`04_Benchmark_methodologie_essentiel.md`](./04_Benchmark_methodologie_essentiel.md) | Règle d'or *comparabilité* : mêmes folds, mêmes métriques, temps mesurés |
| 05 | [`05_Grille_decision_C4_essentiel.md`](./05_Grille_decision_C4_essentiel.md) | Construire la grille de décision C4 (volume, complexité, contraintes, maintenance) |
| 06 | [`06_Menaces_robustesse_essentiel.md`](./06_Menaces_robustesse_essentiel.md) | Acculturation menaces (adversarial, poisoning, OOD) — ouverture M7, non certifiant |
| 07 | [`07_StandardScaler_et_fuites_essentiel.md`](./07_StandardScaler_et_fuites_essentiel.md) | Appui transverse : quand standardiser, scaler dans le `Pipeline`, fuite de prétraitement |

> 🚨 Repère utile : si ton R² dépasse **0.95** sur Bike Sharing, c'est une
> **fuite** (`casual_riders` / `registered_riders` sont des composantes de la
> cible — retire-les). Détail dans le mini-cours `07`.

Liens externes : [`liens_officiels.md`](./liens_officiels.md).
