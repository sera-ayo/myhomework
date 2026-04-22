import sys
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export demo report files for thesis charts and metrics."

    def handle(self, *args, **options):
        scripts_dir = Path(__file__).resolve().parents[5] / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))

        from export_demo_report import main

        main()
        self.stdout.write(self.style.SUCCESS("Metrics export completed."))
