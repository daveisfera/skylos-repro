from django.core.management.base import BaseCommand


def _format_name(name):
    return name.strip().title()


def _unused_export_job():
    return "dead"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(_format_name(options.get("name", "")))
