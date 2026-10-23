"""Django management command — loaded by manage.py via path convention."""


class BaseCommand:
    def handle(self, *args, **options):
        raise NotImplementedError


def _format_msg(name: str) -> str:
    return f"hello, {name}"


class Command(BaseCommand):
    help = "Print a greeting"

    def handle(self, *args, **options):
        name = options.get("name", "world")
        print(_format_msg(name))
