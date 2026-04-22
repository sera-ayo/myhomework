from rest_framework import serializers

from .models import RiskResult, WarningRecord


class RiskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskResult
        fields = [
            "date",
            "rule_score",
            "ml_score",
            "final_score",
            "risk_level",
            "reason_summary",
            "top_reasons_json",
            "model_name",
            "model_version",
            "updated_at",
        ]


class WarningRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningRecord
        fields = [
            "id",
            "warning_time",
            "risk_level",
            "trigger_type",
            "reason_text",
            "action_text",
        ]
