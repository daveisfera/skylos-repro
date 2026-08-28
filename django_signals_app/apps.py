"""AppConfig.ready() imports signals so Django connects @receiver handlers."""

from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "django_signals_app"

    def ready(self):
        from django_signals_app import signals
