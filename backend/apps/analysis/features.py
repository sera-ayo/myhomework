from __future__ import annotations

from statistics import mean

import pandas as pd

from apps.usage.models import DailyUsageAggregate


FEATURE_COLUMNS = [
    "total_duration_sec",
    "launch_count",
    "average_session_sec",
    "longest_session_sec",
    "night_ratio",
    "entertainment_ratio",
    "social_ratio",
    "study_ratio",
    "life_ratio",
    "switch_count",
    "top_app_ratio",
    "weekend_flag",
    "baseline_total_duration_sec",
    "baseline_night_duration_sec",
    "baseline_entertainment_ratio",
    "growth_vs_baseline",
    "night_growth_vs_baseline",
]

LABEL_TO_CLASS = {"low": 0, "medium": 1, "high": 2}
CLASS_TO_SCORE = {0: 20.0, 1: 60.0, 2: 90.0}


def _compute_baselines(*, user_id: int, current_date):
    previous_days = list(
        DailyUsageAggregate.objects.filter(user_id=user_id, date__lt=current_date)
        .order_by("-date")[:7]
    )
    if not previous_days:
        return {
            "baseline_total_duration_sec": 0.0,
            "baseline_night_duration_sec": 0.0,
            "baseline_entertainment_ratio": 0.0,
        }

    return {
        "baseline_total_duration_sec": mean(item.total_duration_sec for item in previous_days),
        "baseline_night_duration_sec": mean(item.night_duration_sec for item in previous_days),
        "baseline_entertainment_ratio": mean(item.entertainment_ratio for item in previous_days),
    }


def feature_row_from_aggregate(aggregate: DailyUsageAggregate) -> dict[str, float]:
    launch_count = aggregate.launch_count or 0
    average_session_sec = (
        aggregate.total_duration_sec / launch_count if launch_count else 0.0
    )
    night_ratio = (
        aggregate.night_duration_sec / aggregate.total_duration_sec
        if aggregate.total_duration_sec
        else 0.0
    )
    baseline = _compute_baselines(user_id=aggregate.user_id, current_date=aggregate.date)
    baseline_total = baseline["baseline_total_duration_sec"]
    baseline_night = baseline["baseline_night_duration_sec"]
    growth_vs_baseline = (
        (aggregate.total_duration_sec - baseline_total) / baseline_total
        if baseline_total
        else 0.0
    )
    night_growth_vs_baseline = (
        (aggregate.night_duration_sec - baseline_night) / baseline_night
        if baseline_night
        else 0.0
    )

    return {
        "total_duration_sec": float(aggregate.total_duration_sec),
        "launch_count": float(aggregate.launch_count),
        "average_session_sec": float(average_session_sec),
        "longest_session_sec": float(aggregate.longest_session_sec),
        "night_ratio": float(night_ratio),
        "entertainment_ratio": float(aggregate.entertainment_ratio),
        "social_ratio": float(aggregate.social_ratio),
        "study_ratio": float(aggregate.study_ratio),
        "life_ratio": float(aggregate.life_ratio),
        "switch_count": float(aggregate.switch_count),
        "top_app_ratio": float(aggregate.top_app_ratio),
        "weekend_flag": float(1 if aggregate.date.weekday() >= 5 else 0),
        "baseline_total_duration_sec": float(baseline_total),
        "baseline_night_duration_sec": float(baseline_night),
        "baseline_entertainment_ratio": float(
            baseline["baseline_entertainment_ratio"]
        ),
        "growth_vs_baseline": float(growth_vs_baseline),
        "night_growth_vs_baseline": float(night_growth_vs_baseline),
    }


def training_frame_from_queryset(queryset) -> pd.DataFrame:
    rows = []
    for aggregate in queryset.order_by("date"):
        row = feature_row_from_aggregate(aggregate)
        row["user_id"] = aggregate.user_id
        row["username"] = aggregate.user.username
        row["date"] = aggregate.date.isoformat()
        rows.append(row)
    if not rows:
        return pd.DataFrame(columns=["user_id", "username", "date", *FEATURE_COLUMNS])
    return pd.DataFrame(rows)
