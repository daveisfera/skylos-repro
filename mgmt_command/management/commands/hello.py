"""Django management command — loaded by manage.py via path convention."""

from django.core.management.base import BaseCommand


def _format_msg(name: str) -> str:
    return f"hello, {name}"


class Command(BaseCommand):
    help = "Print a greeting"

    def add_arguments(self, parser):
        parser.add_argument("--name", default="world")

    def handle(self, *args, **options):
        print(_format_msg(options["name"]))


def unused_export_job():
    return "stale"
