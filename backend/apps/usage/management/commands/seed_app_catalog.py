import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.common.constants import normalize_category, purpose_from_category
from apps.usage.models import AppProfile


class Command(BaseCommand):
    help = "Seed app catalog from demo_data/app_catalog.json"

    def handle(self, *args, **options):
        data_path = Path(__file__).resolve().parents[5] / "demo_data" / "app_catalog.json"
        payload = json.loads(data_path.read_text(encoding="utf-8"))

        created_count = 0
        updated_count = 0
        for item in payload:
            category = normalize_category(item.get("category"))
            defaults = {
                "app_name": item["app_name"],
                "category": category,
                "purpose_group": item.get("purpose_group") or purpose_from_category(category),
            }
            _, created = AppProfile.objects.update_or_create(
                package_name=item["package_name"],
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded app catalog. created={created_count}, updated={updated_count}"
            )
        )
