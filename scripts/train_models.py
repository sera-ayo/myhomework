from __future__ import annotations

import json
from datetime import datetime

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from _bootstrap import ROOT_DIR, setup_django


def metric_row(name: str, y_true, y_pred) -> dict[str, float | str]:
    return {
        "model": name,
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(
            float(precision_score(y_true, y_pred, average="macro", zero_division=0)), 4
        ),
        "recall": round(float(recall_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
    }


def main() -> None:
    setup_django()

    from apps.analysis.features import CLASS_TO_SCORE, FEATURE_COLUMNS
    from apps.analysis.ml import clear_model_cache

    artifacts_dir = ROOT_DIR / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    feature_file = artifacts_dir / "training_features.csv"

    if not feature_file.exists():
        raise RuntimeError("training_features.csv not found. Run build_features.py first.")

    frame = pd.read_csv(feature_file)
    if len(frame) < 9:
        raise RuntimeError("Need at least 9 labeled samples to train the demo models.")

    x = frame[FEATURE_COLUMNS]
    y = frame["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    logistic = LogisticRegression(max_iter=1000)
    random_forest = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    logistic.fit(x_train, y_train)
    random_forest.fit(x_train, y_train)

    logistic_pred = logistic.predict(x_test)
    rf_pred = random_forest.predict(x_test)
    metrics = [
        metric_row("LogisticRegression", y_test, logistic_pred),
        metric_row("RandomForestClassifier", y_test, rf_pred),
    ]

    model_version = datetime.now().strftime("%Y%m%d%H%M%S")
    logistic_bundle = {
        "model": logistic,
        "model_name": "LogisticRegression",
        "model_version": model_version,
        "feature_names": FEATURE_COLUMNS,
        "class_score_mapping": CLASS_TO_SCORE,
    }
    random_forest_bundle = {
        "model": random_forest,
        "model_name": "RandomForestClassifier",
        "model_version": model_version,
        "feature_names": FEATURE_COLUMNS,
        "class_score_mapping": CLASS_TO_SCORE,
    }

    joblib.dump(logistic_bundle, artifacts_dir / "logistic.joblib")
    joblib.dump(random_forest_bundle, artifacts_dir / "random_forest.joblib")
    joblib.dump(random_forest_bundle, artifacts_dir / "active_model.joblib")

    importance_payload = [
        {
            "feature": feature_name,
            "importance": round(float(importance), 6),
        }
        for feature_name, importance in sorted(
            zip(FEATURE_COLUMNS, random_forest.feature_importances_, strict=True),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    metrics_payload = {
        "active_model": "RandomForestClassifier",
        "generated_at": datetime.now().isoformat(),
        "metrics": metrics,
    }

    (artifacts_dir / "metrics.json").write_text(
        json.dumps(metrics_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (artifacts_dir / "feature_importance.json").write_text(
        json.dumps(importance_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    clear_model_cache()
    print(f"Saved models and metrics under {artifacts_dir}")


if __name__ == "__main__":
    main()
