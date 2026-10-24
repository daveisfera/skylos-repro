"""Model method used from a Django template only — no Python call sites / no CBV bridge."""

from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=64)

    def get_display_name(self) -> str:
        return self.name.upper()

    def next_steps_message(self) -> str:
        # Another template-risk helper with no Python callers.
        return f"Review {self.name}"

    class Meta:
        app_label = "model_template"
