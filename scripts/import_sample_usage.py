from __future__ import annotations

from django.core.management import call_command

from _bootstrap import setup_django


def main() -> None:
    setup_django()
    call_command("seed_demo_user")
    call_command("seed_app_catalog")
    call_command("import_sample_usage")


if __name__ == "__main__":
    main()
