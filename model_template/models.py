"""Model methods used only from Django templates — model-method-template-risk."""

from django.db import models


class Record(models.Model):
    STATUS_OPEN = "open"
    STATUS_DONE = "done"
    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_DONE, "Done"),
    )

    name = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)

    def get_display_name(self) -> str:
        return self.name.upper()

    def next_steps_message(self) -> str:
        return f"Review {self.name}"

    def get_current_status_display(self) -> str:
        # Custom display helper (not only auto get_FOO_display).
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    class Meta:
        app_label = "model_template"
