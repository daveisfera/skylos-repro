"""Custom ModelChoiceField — consumer canary: class only referenced by string name
in a type map (and commented form assignment), not as a live class attribute.
"""

from django import forms


class FacilityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "scoreboard_name", str(obj))
