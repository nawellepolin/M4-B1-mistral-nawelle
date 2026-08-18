"""M4-B1 — Évaluation finale du modèle retenu sur le test set."""
from __future__ import annotations

import joblib
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)


def evaluate_final(model_path: Path, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Évalue le modèle retenu sur le test set held-out.

    Args:
        model_path: chemin vers le .joblib du modèle retenu.
        X_test, y_test: test set (jamais vu pendant le benchmark).

    Returns:
        dict avec MAE, RMSE, R².
    """
    model = joblib.load(model_path)
    y_pred = model.predict(X_test)
    return {
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(root_mean_squared_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
    }
