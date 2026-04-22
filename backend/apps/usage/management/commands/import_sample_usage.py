import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.devices.models import Device
from apps.usage.services import ingest_usage_sessions


class Command(BaseCommand):
    help = "Import sample usage sessions from demo_data/sample_sessions.json"

    def handle(self, *args, **options):
        user_model = get_user_model()
        user = user_model.objects.filter(username="demo").first()
        if user is None:
            raise CommandError("Demo user does not exist. Run seed_demo_user first.")

        data_path = Path(__file__).resolve().parents[5] / "demo_data" / "sample_sessions.json"
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        device_code = payload["device_code"]

        Device.objects.update_or_create(
            device_code=device_code,
            defaults={
                "user": user,
                "brand": payload.get("brand", "Google"),
                "model": payload.get("model", "Pixel Demo"),
                "android_version": payload.get("android_version", "14"),
            },
        )

        result = ingest_usage_sessions(
            user=user,
            payload={
                "device_code": device_code,
                "source": "sample",
                "sessions": payload["sessions"],
            },
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Imported sample sessions. "
                f"created={result['created_count']}, duplicates={result['duplicate_count']}"
            )
        )
