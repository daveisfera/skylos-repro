"""Form that declares the custom field — only reference to FacilityChoiceField."""

from django import forms

from django_form_field.fields import FacilityChoiceField


class JoinFacilityForm(forms.Form):
    facility = FacilityChoiceField(required=True)
