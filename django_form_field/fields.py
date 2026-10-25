"""Custom ModelChoiceField — used only as a form attribute."""

from django import forms


class FacilityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "scoreboard_name", str(obj))

    def clean(self, value):
        return super().clean(value)
