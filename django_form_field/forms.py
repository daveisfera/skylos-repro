"""Form that declares the custom field."""

from django import forms

from django_form_field.fields import FacilityChoiceField


class JoinFacilityForm(forms.Form):
    facility = FacilityChoiceField(queryset=None, required=True)
