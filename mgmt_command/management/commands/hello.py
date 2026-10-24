"""Management command helper passed to Django autoreload — web-server celery_watch shape."""

from django.core.management.base import BaseCommand
from django.utils import autoreload


def _restart_worker(name, queue):
    # Live: passed to autoreload.run_with_reloader (not called directly).
    print(f"restart {name} on {queue}")


class Command(BaseCommand):
    help = "Restart a worker on code changes"

    def add_arguments(self, parser):
        parser.add_argument("-Q", "--queue", required=True)
        parser.add_argument("-n", "--name", required=True)

    def handle(self, *args, **options):
        autoreload.run_with_reloader(
            _restart_worker, options["name"], options["queue"]
        )
