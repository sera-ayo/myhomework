from django.conf import settings
from django.db import models

from apps.common.constants import CATEGORY_CHOICES, PURPOSE_CHOICES


class AppProfile(models.Model):
    package_name = models.CharField(max_length=255, unique=True)
    app_name = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="other")
    purpose_group = models.CharField(
        max_length=32,
        choices=PURPOSE_CHOICES,
        default="life",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["package_name"]

    def __str__(self) -> str:
        return f"{self.app_name} ({self.package_name})"


class UsageSession(models.Model):
    SOURCE_CHOICES = (
        ("android", "Android"),
        ("sample", "Sample"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="usage_sessions",
    )
    device = models.ForeignKey(
        "devices.Device",
        on_delete=models.CASCADE,
        related_name="usage_sessions",
    )
    package_name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="other")
    purpose_group = models.CharField(
        max_length=32,
        choices=PURPOSE_CHOICES,
        default="life",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_sec = models.PositiveIntegerField()
    is_night_session = models.BooleanField(default=False)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES, default="android")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "device", "package_name", "start_time", "end_time"],
                name="unique_usage_session",
            )
        ]
        indexes = [
            models.Index(fields=["user", "start_time"]),
            models.Index(fields=["device", "start_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.app_name} {self.start_time} ({self.duration_sec}s)"


class DailyUsageAggregate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_usage_aggregates",
    )
    date = models.DateField()
    total_duration_sec = models.PositiveIntegerField(default=0)
    launch_count = models.PositiveIntegerField(default=0)
    night_duration_sec = models.PositiveIntegerField(default=0)
    longest_session_sec = models.PositiveIntegerField(default=0)
    entertainment_ratio = models.FloatField(default=0.0)
    social_ratio = models.FloatField(default=0.0)
    study_ratio = models.FloatField(default=0.0)
    life_ratio = models.FloatField(default=0.0)
    switch_count = models.PositiveIntegerField(default=0)
    top_app_name = models.CharField(max_length=128, blank=True)
    top_app_ratio = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_daily_usage_aggregate",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.date}"
