from __future__ import annotations

from typing import Final


CATEGORY_CHOICES: Final[tuple[tuple[str, str], ...]] = (
    ("short_video", "短视频"),
    ("social", "社交"),
    ("study", "学习"),
    ("tool", "工具"),
    ("video_music", "视频音乐"),
    ("game", "游戏"),
    ("shopping", "购物"),
    ("other", "其他"),
)

PURPOSE_CHOICES: Final[tuple[tuple[str, str], ...]] = (
    ("entertainment", "娱乐"),
    ("social", "社交"),
    ("study", "学习"),
    ("life", "生活"),
)

RISK_LEVEL_CHOICES: Final[tuple[tuple[str, str], ...]] = (
    ("low", "低风险"),
    ("medium", "中风险"),
    ("high", "高风险"),
)

CATEGORY_TO_PURPOSE: Final[dict[str, str]] = {
    "short_video": "entertainment",
    "video_music": "entertainment",
    "game": "entertainment",
    "social": "social",
    "study": "study",
    "tool": "life",
    "shopping": "life",
    "other": "life",
}

RISK_LEVEL_LABELS: Final[dict[str, str]] = dict(RISK_LEVEL_CHOICES)
CATEGORY_LABELS: Final[dict[str, str]] = dict(CATEGORY_CHOICES)
PURPOSE_LABELS: Final[dict[str, str]] = dict(PURPOSE_CHOICES)


def normalize_category(raw_value: str | None) -> str:
    if not raw_value:
        return "other"
    normalized = raw_value.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in CATEGORY_TO_PURPOSE:
        return normalized
    return "other"


def purpose_from_category(category: str | None) -> str:
    normalized = normalize_category(category)
    return CATEGORY_TO_PURPOSE.get(normalized, "life")
