"""Model method used from a Django template, not from Python call sites."""

from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=64)

    def get_display_name(self) -> str:
        return self.name.upper()

    class Meta:
        app_label = "model_template"
