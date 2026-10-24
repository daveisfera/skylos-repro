"""Custom ModelChoiceField — mirrors modernstat.msfacility.fields.FacilityChoiceField."""

from django import forms


class FacilityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "scoreboard_name", str(obj))
