"""M4-B1 — Boucle benchmark 3+ familles de modèles.

Règle d'or *comparabilité* (mini-cours 04) :
- **Mêmes folds** pour tous les modèles (même `cv`)
- **Mêmes métriques** (MAE, RMSE, R²)
- **Même prétraitement** appliqué uniformément

Anti-fuite : `run_benchmark` ré-instancie chaque modèle par fold puis le `fit`
sur les seules données d'entraînement du fold. Tout prétraitement **qui apprend
des paramètres** (ex. `StandardScaler`) doit donc vivre DANS la factory du
modèle (`make_pipeline(StandardScaler(), estimator)`), jamais être appliqué à
`X` en amont — sinon le scaler « voit » le fold de test (fuite de données).

À compléter :
- TODO 1 : import + définir 3 modèles à benchmarker (3 familles différentes) ;
  pour le linéaire, encapsuler le scaler via `make_pipeline` (anti-fuite)
- TODO 2 : choix `KFold` vs `TimeSeriesSplit` (justifie dans le notebook)
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

# TODO 1 — Imports des 3+ modèles
# from sklearn.linear_model import Ridge
# from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

# TODO 2 — Choix du splitter (justifie en notebook)
# from sklearn.model_selection import KFold, TimeSeriesSplit


@dataclass
class BenchmarkResult:
    """Résultat d'un benchmark sur 1 modèle, 1 split."""

    model_name: str
    mae: float
    rmse: float
    r2: float
    fit_time_sec: float
    predict_time_ms_per_1k: float


def benchmark_one(
    model,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> BenchmarkResult:
    """Entraîne 1 modèle sur 1 fold, retourne ses métriques.

    Args:
        model: estimator sklearn (avec .fit et .predict).
        X_train, y_train: données d'entraînement.
        X_test, y_test: données de test (1 fold).

    Returns:
        BenchmarkResult avec MAE, RMSE, R², temps train, temps predict.
    """
    # Fit
    t0 = time.perf_counter()
    model.fit(X_train, y_train)
    fit_time = time.perf_counter() - t0

    # Predict (mesure latence sur 1k échantillons pour comparaison fair)
    n_pred = min(1000, len(X_test))
    X_pred = X_test.iloc[:n_pred]
    t0 = time.perf_counter()
    _ = model.predict(X_pred)
    pred_time = (time.perf_counter() - t0) * 1000  # en ms

    # Métriques sur le fold complet
    y_pred_full = model.predict(X_test)
    return BenchmarkResult(
        model_name=type(model).__name__,
        mae=float(mean_absolute_error(y_test, y_pred_full)),
        rmse=float(root_mean_squared_error(y_test, y_pred_full)),
        r2=float(r2_score(y_test, y_pred_full)),
        fit_time_sec=fit_time,
        predict_time_ms_per_1k=pred_time,
    )


def run_benchmark(
    models: dict,
    X: pd.DataFrame,
    y: pd.Series,
    splitter,
) -> pd.DataFrame:
    """Lance le benchmark de plusieurs modèles avec le **même splitter**.

    Args:
        models: dict {nom: estimator}.
        X, y: dataset complet.
        splitter: sklearn splitter (KFold, TimeSeriesSplit, ...).

    Returns:
        DataFrame avec moyennes par modèle sur tous les folds.
    """
    rows = []
    for fold_idx, (train_idx, test_idx) in enumerate(splitter.split(X, y)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        for name, model_factory in models.items():
            model = model_factory()  # nouvelle instance par fold
            result = benchmark_one(model, X_train, y_train, X_test, y_test)
            rows.append({
                "model": name,
                "fold": fold_idx,
                "mae": result.mae,
                "rmse": result.rmse,
                "r2": result.r2,
                "fit_time_sec": result.fit_time_sec,
                "predict_time_ms_per_1k": result.predict_time_ms_per_1k,
            })

    df = pd.DataFrame(rows)
    # Moyenne par modèle
    summary = df.groupby("model").agg({
        "mae": "mean",
        "rmse": "mean",
        "r2": "mean",
        "fit_time_sec": "mean",
        "predict_time_ms_per_1k": "mean",
    }).round(4)
    return summary
