from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.analysis.services import rebuild_daily_analysis_for_dates
from apps.usage.models import UsageSession


class Command(BaseCommand):
    help = "Rebuild daily aggregates and risk results for a user."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="Target username")

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options["username"]).first()
        if user is None:
            raise CommandError("User not found.")

        dates = sorted(
            {
                timezone.localtime(start_time).date()
                for start_time in UsageSession.objects.filter(user=user).values_list(
                    "start_time",
                    flat=True,
                )
            }
        )
        rebuild_daily_analysis_for_dates(user=user, dates=sorted(dates))
        self.stdout.write(
            self.style.SUCCESS(
                f"Rebuilt aggregates and risk results for {user.username}: {len(dates)} days"
            )
        )
