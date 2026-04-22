from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.analysis.ml import clear_model_cache
from apps.analysis.services import rebuild_single_day_analysis
from apps.devices.models import Device
from apps.usage.models import DailyUsageAggregate, UsageSession
from apps.warnings.models import RiskResult


class DemoApiFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_user")
        call_command("seed_app_catalog")
        call_command("import_sample_usage")
        call_command("rebuild_aggregates", username="demo")

    def setUp(self):
        self.client = APIClient()
        response = self.client.post(
            "/api/auth/login",
            {"username": "demo", "password": "demo123456"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_dashboard_and_warning_endpoints_return_data(self):
        summary = self.client.get("/api/dashboard/summary")
        trend = self.client.get("/api/dashboard/trend?days=30")
        categories = self.client.get("/api/dashboard/categories")
        risk = self.client.get("/api/risk/latest")
        warnings = self.client.get("/api/warnings/list")
        metrics = self.client.get("/api/experiments/metrics")

        self.assertEqual(summary.status_code, 200)
        self.assertTrue(summary.json()["available"])
        self.assertEqual(trend.status_code, 200)
        self.assertEqual(len(trend.json()["items"]), 30)
        self.assertEqual(categories.status_code, 200)
        self.assertTrue(categories.json()["available"])
        self.assertEqual(risk.status_code, 200)
        self.assertTrue(risk.json()["available"])
        self.assertEqual(warnings.status_code, 200)
        self.assertGreater(len(warnings.json()["items"]), 0)
        self.assertEqual(metrics.status_code, 200)

    def test_duplicate_upload_does_not_duplicate_sessions(self):
        user_model = get_user_model()
        uploader = user_model.objects.create_user(username="api_user", password="demo123456")
        login = self.client.post(
            "/api/auth/login",
            {"username": "api_user", "password": "demo123456"},
            format="json",
        )
        token = login.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        device_payload = {
            "device_code": "api-device-001",
            "brand": "Google",
            "model": "Pixel",
            "android_version": "14",
        }
        device_response = self.client.post("/api/devices/register", device_payload, format="json")
        self.assertEqual(device_response.status_code, 200)

        now = timezone.now().replace(microsecond=0)
        upload_payload = {
            "device_code": "api-device-001",
            "sessions": [
                {
                    "package_name": "com.ss.android.ugc.aweme",
                    "app_name": "抖音",
                    "category": "short_video",
                    "start_time": (now - timedelta(minutes=30)).isoformat(),
                    "end_time": now.isoformat(),
                    "duration_sec": 1800,
                }
            ],
        }

        first = self.client.post("/api/usage/sessions/bulk", upload_payload, format="json")
        second = self.client.post("/api/usage/sessions/bulk", upload_payload, format="json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json()["created_count"], 1)
        self.assertEqual(second.json()["created_count"], 0)
        self.assertEqual(second.json()["duplicate_count"], 1)
        self.assertEqual(UsageSession.objects.filter(user=uploader).count(), 1)
        self.assertEqual(DailyUsageAggregate.objects.filter(user=uploader).count(), 1)
        self.assertEqual(RiskResult.objects.filter(user=uploader).count(), 1)


class RuleFallbackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="fallback_user", password="demo123456")
        self.device = Device.objects.create(
            user=self.user,
            device_code="fallback-device",
            brand="Google",
            model="Pixel",
            android_version="14",
        )

    def test_missing_model_file_falls_back_to_rule_engine(self):
        start_time = timezone.now().replace(microsecond=0)
        UsageSession.objects.create(
            user=self.user,
            device=self.device,
            package_name="com.ss.android.ugc.aweme",
            app_name="抖音",
            category="short_video",
            purpose_group="entertainment",
            start_time=start_time,
            end_time=start_time + timedelta(minutes=80),
            duration_sec=4800,
            is_night_session=True,
            source="sample",
        )

        with patch("apps.analysis.ml.active_model_path", return_value=Path("/tmp/nonexistent-model.joblib")):
            clear_model_cache()
            aggregate = rebuild_single_day_analysis(
                user=self.user,
                day=timezone.localtime(start_time).date(),
                device=self.device,
            )
            self.assertIsNotNone(aggregate)

        result = RiskResult.objects.get(user=self.user)
        self.assertEqual(result.model_name, "rule_engine")
        self.assertEqual(result.model_version, "builtin")
        self.assertIsNone(result.ml_score)
