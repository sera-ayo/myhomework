from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings

from .features import CLASS_TO_SCORE, FEATURE_COLUMNS


def artifacts_dir() -> Path:
    return Path(settings.BASE_DIR).parent / "artifacts"


def metrics_path() -> Path:
    return artifacts_dir() / "metrics.json"


def feature_importance_path() -> Path:
    return artifacts_dir() / "feature_importance.json"


def active_model_path() -> Path:
    return artifacts_dir() / "active_model.joblib"


@lru_cache(maxsize=1)
def _load_active_model_bundle():
    path = active_model_path()
    if not path.exists():
        return None
    return joblib.load(path)


def clear_model_cache() -> None:
    _load_active_model_bundle.cache_clear()


def read_metrics() -> dict:
    path = metrics_path()
    if not path.exists():
        return {
            "available": False,
            "active_model": "rule_engine",
            "metrics": {},
            "feature_importance": [],
        }

    payload = json.loads(path.read_text(encoding="utf-8"))
    feature_importance = []
    if feature_importance_path().exists():
        feature_importance = json.loads(
            feature_importance_path().read_text(encoding="utf-8")
        )

    payload["available"] = True
    payload["feature_importance"] = feature_importance
    return payload


def predict_ml_score(feature_row: dict[str, float]) -> dict | None:
    bundle = _load_active_model_bundle()
    if bundle is None:
        return None

    model = bundle["model"]
    feature_names = bundle.get("feature_names", FEATURE_COLUMNS)
    class_score_mapping = bundle.get("class_score_mapping", CLASS_TO_SCORE)
    frame = pd.DataFrame([feature_row])[feature_names]
    probabilities = model.predict_proba(frame)[0]
    classes = model.classes_

    ml_score = 0.0
    for index, class_label in enumerate(classes):
        ml_score += probabilities[index] * class_score_mapping[int(class_label)]

    return {
        "ml_score": round(float(ml_score), 2),
        "model_name": bundle.get("model_name", model.__class__.__name__),
        "model_version": bundle.get("model_version", "unversioned"),
    }
