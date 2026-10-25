from django.apps import AppConfig


class ReceiverSignalsConfig(AppConfig):
    name = "receiver_signals"
    default = True

    def ready(self):
        from receiver_signals import signals  # noqa: F401
