from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from _bootstrap import ROOT_DIR, setup_django


def main() -> None:
    setup_django()

    from apps.usage.models import DailyUsageAggregate
    from apps.warnings.models import RiskResult

    artifacts_dir = ROOT_DIR / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    aggregates = pd.DataFrame(
        list(
            DailyUsageAggregate.objects.values(
                "date",
                "total_duration_sec",
                "night_duration_sec",
                "entertainment_ratio",
                "social_ratio",
                "study_ratio",
                "life_ratio",
                "top_app_name",
            )
        )
    )
    risks = pd.DataFrame(
        list(
            RiskResult.objects.values(
                "date",
                "rule_score",
                "ml_score",
                "final_score",
                "risk_level",
            )
        )
    )

    aggregates.to_csv(artifacts_dir / "report_aggregates.csv", index=False)
    risks.to_csv(artifacts_dir / "report_risks.csv", index=False)

    summary = {
        "aggregate_rows": len(aggregates),
        "risk_rows": len(risks),
    }
    (artifacts_dir / "report_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Exported demo report files to {artifacts_dir}")


if __name__ == "__main__":
    main()
