"""Form that does NOT keep FacilityChoiceField live via a class attribute.

Production BoardForm only had FacilityChoiceField in a commented __init__ block;
the live reference is the string key in ANGULAR_TEMPLATES.
"""

from django import forms

# from django_form_field.fields import FacilityChoiceField


class JoinFacilityForm(forms.Form):
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Commented production shape — do not uncomment (would quiet the canary):
        # self.fields["group_facility"] = FacilityChoiceField(
        #     label="Private to Facility",
        #     queryset=None,
        #     required=False,
        # )
