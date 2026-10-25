from django.apps import AppConfig


class PkgConfig(AppConfig):
    name = "pkg"

    def ready(self):
        from pkg.feature import signals  # noqa: F401
