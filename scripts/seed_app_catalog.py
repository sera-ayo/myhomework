from __future__ import annotations

from django.core.management import call_command

from _bootstrap import setup_django


def main() -> None:
    setup_django()
    call_command("seed_app_catalog")


if __name__ == "__main__":
    main()
