from __future__ import annotations

from collections import defaultdict

from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from apps.common.constants import normalize_category, purpose_from_category
from apps.devices.models import Device

from .models import AppProfile, UsageSession


def _is_night_session(start_time) -> bool:
    local_start = timezone.localtime(start_time)
    return local_start.hour >= 22 or local_start.hour < 6


def _coerce_datetime(value):
    if hasattr(value, "utcoffset"):
        if timezone.is_naive(value):
            return timezone.make_aware(value, timezone.get_current_timezone())
        return value

    parsed = parse_datetime(value)
    if parsed is None:
        raise ValueError(f"无法解析时间字段: {value}")
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def _resolve_profile(package_name: str, app_name: str, raw_category: str | None) -> tuple[str, str]:
    profile = AppProfile.objects.filter(package_name=package_name).first()
    if profile:
        if app_name and profile.app_name != app_name:
            profile.app_name = app_name
            profile.save(update_fields=["app_name", "updated_at"])
        return profile.category, profile.purpose_group

    category = normalize_category(raw_category)
    purpose_group = purpose_from_category(category)
    AppProfile.objects.create(
        package_name=package_name,
        app_name=app_name,
        category=category,
        purpose_group=purpose_group,
    )
    return category, purpose_group


@transaction.atomic
def ingest_usage_sessions(*, user, payload: dict) -> dict:
    device = Device.objects.filter(user=user, device_code=payload["device_code"]).first()
    if not device:
        raise ValueError("设备未注册。")

    created_count = 0
    duplicate_count = 0
    touched_dates = set()

    for session in payload["sessions"]:
        start_time = _coerce_datetime(session["start_time"])
        end_time = _coerce_datetime(session["end_time"])
        category, purpose_group = _resolve_profile(
            package_name=session["package_name"],
            app_name=session["app_name"],
            raw_category=session.get("category"),
        )
        usage_session, created = UsageSession.objects.get_or_create(
            user=user,
            device=device,
            package_name=session["package_name"],
            start_time=start_time,
            end_time=end_time,
            defaults={
                "app_name": session["app_name"],
                "category": category,
                "purpose_group": purpose_group,
                "duration_sec": session["duration_sec"],
                "is_night_session": _is_night_session(start_time),
                "source": payload.get("source", "android"),
            },
        )
        if created:
            created_count += 1
            touched_dates.add(timezone.localtime(start_time).date())
        else:
            duplicate_count += 1
            if usage_session.duration_sec != session["duration_sec"]:
                usage_session.duration_sec = session["duration_sec"]
                usage_session.save(update_fields=["duration_sec"])

    device.last_sync_at = timezone.now()
    device.save(update_fields=["last_sync_at", "updated_at"])

    from apps.analysis.services import rebuild_daily_analysis_for_dates

    rebuild_daily_analysis_for_dates(user=user, dates=sorted(touched_dates), device=device)
    return {
        "device": device,
        "created_count": created_count,
        "duplicate_count": duplicate_count,
        "processed_dates": sorted(str(item) for item in touched_dates),
    }


def summarize_category_durations(sessions) -> dict[str, int]:
    durations: dict[str, int] = defaultdict(int)
    for session in sessions:
        durations[session.purpose_group] += session.duration_sec
    return durations
