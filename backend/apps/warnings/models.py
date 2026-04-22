from django.conf import settings
from django.db import models

from apps.common.constants import RISK_LEVEL_CHOICES


class RiskResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="risk_results",
    )
    date = models.DateField()
    rule_score = models.FloatField(default=0.0)
    ml_score = models.FloatField(null=True, blank=True)
    final_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=16, choices=RISK_LEVEL_CHOICES, default="low")
    reason_summary = models.TextField(blank=True)
    top_reasons_json = models.JSONField(default=list, blank=True)
    model_name = models.CharField(max_length=64, default="rule_engine")
    model_version = models.CharField(max_length=64, default="builtin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_risk_result_per_day",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.date} {self.risk_level}"


class WarningRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="warning_records",
    )
    device = models.ForeignKey(
        "devices.Device",
        on_delete=models.SET_NULL,
        related_name="warning_records",
        null=True,
        blank=True,
    )
    warning_time = models.DateTimeField()
    risk_level = models.CharField(max_length=16, choices=RISK_LEVEL_CHOICES, default="low")
    trigger_type = models.CharField(max_length=32, default="daily_analysis")
    reason_text = models.TextField()
    action_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-warning_time"]
        indexes = [models.Index(fields=["user", "warning_time"])]

    def __str__(self) -> str:
        return f"{self.user} {self.warning_time} {self.risk_level}"
