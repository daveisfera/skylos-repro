"""Helpers called from Command.handle — leftover mgmt noise after Command class is quiet."""

from django.core.management.base import BaseCommand


def _format_name(name: str) -> str:
    return name.strip().title()


def _dead_helper():
    # Intentional true positive — nothing in this module calls it.
    return "stale"


class Command(BaseCommand):
    help = "Greet"

    def add_arguments(self, parser):
        parser.add_argument("--name", default="world")

    def handle(self, *args, **options):
        self.stdout.write(_format_name(options["name"]))
