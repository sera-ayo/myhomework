from __future__ import annotations

from collections import defaultdict
from datetime import datetime, time
from statistics import mean

from django.db.models import Max
from django.utils import timezone

from apps.common.constants import PURPOSE_LABELS, RISK_LEVEL_LABELS
from apps.devices.models import Device
from apps.usage.models import DailyUsageAggregate, UsageSession
from apps.warnings.models import RiskResult, WarningRecord

from .features import feature_row_from_aggregate
from .ml import predict_ml_score, read_metrics


def _day_bounds(day):
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.combine(day, time.min), tz)
    end = timezone.make_aware(datetime.combine(day, time.max), tz)
    return start, end


def _build_reason(key: str, points: int, detail: str) -> dict[str, str | int]:
    return {"key": key, "points": points, "detail": detail}


def _compute_rule_result(*, user, aggregate: DailyUsageAggregate) -> tuple[float, list[dict]]:
    reasons: list[dict] = []
    score = 0

    if aggregate.total_duration_sec > 6 * 3600:
        score += 25
        reasons.append(_build_reason("total_duration", 25, "当日总使用时长超过 6 小时。"))
    elif aggregate.total_duration_sec >= 4 * 3600:
        score += 15
        reasons.append(_build_reason("total_duration", 15, "当日总使用时长已超过 4 小时。"))

    if aggregate.night_duration_sec > 90 * 60:
        score += 20
        reasons.append(_build_reason("night_duration", 20, "夜间使用时长超过 90 分钟。"))
    elif aggregate.night_duration_sec >= 30 * 60:
        score += 10
        reasons.append(_build_reason("night_duration", 10, "夜间使用时长已超过 30 分钟。"))

    if aggregate.entertainment_ratio > 0.6:
        score += 20
        reasons.append(_build_reason("entertainment_ratio", 20, "娱乐类应用占比超过 60%。"))
    elif aggregate.entertainment_ratio >= 0.4:
        score += 10
        reasons.append(_build_reason("entertainment_ratio", 10, "娱乐类应用占比超过 40%。"))

    if aggregate.longest_session_sec > 60 * 60:
        score += 15
        reasons.append(
            _build_reason("longest_session", 15, "单次连续使用时长超过 60 分钟。")
        )
    elif aggregate.longest_session_sec >= 30 * 60:
        score += 8
        reasons.append(
            _build_reason("longest_session", 8, "单次连续使用时长超过 30 分钟。")
        )

    if aggregate.switch_count > 80:
        score += 10
        reasons.append(_build_reason("switch_count", 10, "应用切换次数超过 80 次。"))
    elif aggregate.switch_count >= 40:
        score += 5
        reasons.append(_build_reason("switch_count", 5, "应用切换次数超过 40 次。"))

    baseline_days = list(
        DailyUsageAggregate.objects.filter(user=user, date__lt=aggregate.date)
        .order_by("-date")[:7]
    )
    baseline_average = mean(item.total_duration_sec for item in baseline_days) if baseline_days else 0
    if baseline_average:
        growth_ratio = (aggregate.total_duration_sec - baseline_average) / baseline_average
        if growth_ratio > 0.3:
            score += 10
            reasons.append(
                _build_reason("growth", 10, "相较近 7 日平均水平，使用总时长增长超过 30%。")
            )

    return float(score), sorted(reasons, key=lambda item: item["points"], reverse=True)


def _risk_level_from_score(final_score: float) -> str:
    if final_score >= 70:
        return "high"
    if final_score >= 35:
        return "medium"
    return "low"


def _reason_summary(reasons: list[dict]) -> str:
    if not reasons:
        return "当前行为整体稳定，未触发明显风险项。"
    return "；".join(item["detail"] for item in reasons[:3])


def _action_text(risk_level: str) -> str:
    if risk_level == "high":
        return "建议立即休息 10 分钟，并减少娱乐类应用使用。"
    if risk_level == "medium":
        return "建议关注今日使用习惯，适当切换到学习或生活类应用。"
    return "建议保持当前节奏，继续关注夜间和连续使用时长。"


def rebuild_daily_analysis_for_dates(*, user, dates: list, device: Device | None = None) -> None:
    for current_date in dates:
        rebuild_single_day_analysis(user=user, day=current_date, device=device)


def rebuild_single_day_analysis(*, user, day, device: Device | None = None) -> DailyUsageAggregate | None:
    start, end = _day_bounds(day)
    sessions = list(
        UsageSession.objects.filter(user=user, start_time__gte=start, start_time__lte=end)
        .order_by("start_time")
    )

    if not sessions:
        DailyUsageAggregate.objects.filter(user=user, date=day).delete()
        RiskResult.objects.filter(user=user, date=day).delete()
        WarningRecord.objects.filter(user=user, warning_time__date=day).delete()
        return None

    total_duration = sum(item.duration_sec for item in sessions)
    launch_count = len(sessions)
    night_duration = sum(item.duration_sec for item in sessions if item.is_night_session)
    longest_session = max(item.duration_sec for item in sessions)
    switch_count = max(launch_count - 1, 0)

    purpose_duration: dict[str, int] = defaultdict(int)
    app_duration: dict[str, int] = defaultdict(int)
    for session in sessions:
        purpose_duration[session.purpose_group] += session.duration_sec
        app_duration[session.app_name] += session.duration_sec

    top_app_name = ""
    top_app_ratio = 0.0
    if app_duration:
        top_app_name, top_app_duration = max(app_duration.items(), key=lambda item: item[1])
        top_app_ratio = top_app_duration / total_duration if total_duration else 0.0

    aggregate, _ = DailyUsageAggregate.objects.update_or_create(
        user=user,
        date=day,
        defaults={
            "total_duration_sec": total_duration,
            "launch_count": launch_count,
            "night_duration_sec": night_duration,
            "longest_session_sec": longest_session,
            "entertainment_ratio": purpose_duration["entertainment"] / total_duration
            if total_duration
            else 0.0,
            "social_ratio": purpose_duration["social"] / total_duration if total_duration else 0.0,
            "study_ratio": purpose_duration["study"] / total_duration if total_duration else 0.0,
            "life_ratio": purpose_duration["life"] / total_duration if total_duration else 0.0,
            "switch_count": switch_count,
            "top_app_name": top_app_name,
            "top_app_ratio": top_app_ratio,
        },
    )

    rule_score, reasons = _compute_rule_result(user=user, aggregate=aggregate)
    ml_result = predict_ml_score(feature_row_from_aggregate(aggregate))
    if ml_result is None:
        final_score = rule_score
        model_name = "rule_engine"
        model_version = "builtin"
        ml_score = None
    else:
        ml_score = ml_result["ml_score"]
        final_score = round(0.4 * rule_score + 0.6 * ml_score, 2)
        model_name = ml_result["model_name"]
        model_version = ml_result["model_version"]

    risk_level = _risk_level_from_score(final_score)
    RiskResult.objects.update_or_create(
        user=user,
        date=day,
        defaults={
            "rule_score": rule_score,
            "ml_score": ml_score,
            "final_score": final_score,
            "risk_level": risk_level,
            "reason_summary": _reason_summary(reasons),
            "top_reasons_json": reasons[:3],
            "model_name": model_name,
            "model_version": model_version,
        },
    )

    WarningRecord.objects.filter(user=user, trigger_type="daily_analysis", warning_time__date=day).delete()
    if risk_level in {"medium", "high"}:
        warning_time = timezone.make_aware(datetime.combine(day, time(hour=21, minute=0)))
        WarningRecord.objects.create(
            user=user,
            device=device,
            warning_time=warning_time,
            risk_level=risk_level,
            trigger_type="daily_analysis",
            reason_text=_reason_summary(reasons),
            action_text=_action_text(risk_level),
        )
    return aggregate


def dashboard_summary_for_user(user) -> dict:
    latest_aggregate = DailyUsageAggregate.objects.filter(user=user).order_by("-date").first()
    if latest_aggregate is None:
        return {
            "available": False,
            "message": "暂无使用数据，请先导入样例或同步真机数据。",
        }

    latest_risk = RiskResult.objects.filter(user=user, date=latest_aggregate.date).first()
    recent_days = list(
        DailyUsageAggregate.objects.filter(user=user).order_by("-date")[:7]
    )
    average_7d = mean(item.total_duration_sec for item in recent_days) if recent_days else 0
    return {
        "available": True,
        "date": latest_aggregate.date,
        "total_duration_sec": latest_aggregate.total_duration_sec,
        "launch_count": latest_aggregate.launch_count,
        "top_app_name": latest_aggregate.top_app_name,
        "top_app_ratio": round(latest_aggregate.top_app_ratio, 4),
        "seven_day_avg_duration_sec": round(average_7d, 2),
        "risk_level": latest_risk.risk_level if latest_risk else "low",
        "risk_label": RISK_LEVEL_LABELS.get(
            latest_risk.risk_level if latest_risk else "low",
            "低风险",
        ),
        "final_score": latest_risk.final_score if latest_risk else 0.0,
        "reason_summary": latest_risk.reason_summary if latest_risk else "",
    }


def dashboard_trend_for_user(user, *, days: int) -> list[dict]:
    aggregates = list(
        DailyUsageAggregate.objects.filter(user=user).order_by("-date")[:days]
    )
    aggregate_map = {item.date: item for item in aggregates}
    risk_map = {
        item.date: item
        for item in RiskResult.objects.filter(user=user, date__in=aggregate_map.keys())
    }
    rows = []
    for aggregate in reversed(aggregates):
        risk = risk_map.get(aggregate.date)
        rows.append(
            {
                "date": aggregate.date.isoformat(),
                "total_duration_sec": aggregate.total_duration_sec,
                "night_duration_sec": aggregate.night_duration_sec,
                "final_score": risk.final_score if risk else 0.0,
                "risk_level": risk.risk_level if risk else "low",
            }
        )
    return rows


def dashboard_categories_for_user(user, *, day=None) -> dict:
    aggregate = (
        DailyUsageAggregate.objects.filter(user=user, date=day).first()
        if day
        else DailyUsageAggregate.objects.filter(user=user).order_by("-date").first()
    )
    if aggregate is None:
        return {"available": False, "date": None, "categories": []}

    categories = [
        {
            "key": "entertainment",
            "label": PURPOSE_LABELS["entertainment"],
            "ratio": round(aggregate.entertainment_ratio, 4),
        },
        {
            "key": "social",
            "label": PURPOSE_LABELS["social"],
            "ratio": round(aggregate.social_ratio, 4),
        },
        {
            "key": "study",
            "label": PURPOSE_LABELS["study"],
            "ratio": round(aggregate.study_ratio, 4),
        },
        {
            "key": "life",
            "label": PURPOSE_LABELS["life"],
            "ratio": round(aggregate.life_ratio, 4),
        },
    ]
    return {"available": True, "date": aggregate.date.isoformat(), "categories": categories}


def experiments_payload() -> dict:
    return read_metrics()
