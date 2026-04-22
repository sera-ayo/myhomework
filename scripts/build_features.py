from __future__ import annotations

from pathlib import Path

import pandas as pd
from django.contrib.auth import get_user_model

from _bootstrap import ROOT_DIR, setup_django


def main() -> None:
    setup_django()

    from apps.analysis.features import LABEL_TO_CLASS, training_frame_from_queryset
    from apps.usage.models import DailyUsageAggregate

    labels_path = ROOT_DIR / "demo_data" / "sample_labels.csv"
    output_path = ROOT_DIR / "artifacts" / "training_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = pd.read_csv(labels_path)
    labels["date"] = labels["date"].astype(str)
    labels["target"] = labels["label"].map(LABEL_TO_CLASS)

    queryset = DailyUsageAggregate.objects.select_related("user").all()
    frame = training_frame_from_queryset(queryset)
    if frame.empty:
        raise RuntimeError("No aggregates found. Import sample or real usage data first.")

    merged = frame.merge(labels, on=["username", "date"], how="inner")
    merged.to_csv(output_path, index=False)
    print(f"Saved features to {output_path}")


if __name__ == "__main__":
    main()
