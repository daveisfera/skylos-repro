"""Custom form field — used only as a Form class attribute."""

from django import forms


class FacilityChoiceField(forms.Field):
    """Subclass kept for form declarations."""

    def clean(self, value):
        return value
