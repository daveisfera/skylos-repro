"""Form that declares the custom field — only reference to FacilityChoiceField."""

from fields import FacilityChoiceField


class JoinFacilityForm:
    facility = FacilityChoiceField(required=True)
