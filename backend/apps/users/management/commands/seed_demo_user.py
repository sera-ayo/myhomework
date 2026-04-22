from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the demo user account."

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username="demo")
        user.set_password("demo123456")
        user.is_staff = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Created demo user demo/demo123456"))
        else:
            self.stdout.write(self.style.SUCCESS("Updated demo user password to demo123456"))
