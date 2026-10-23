"""Custom form field — used only as a Form class attribute."""


class Field:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class FacilityChoiceField(Field):
    """Subclass kept for form declarations; no direct call sites."""

    def clean(self, value):
        return value
