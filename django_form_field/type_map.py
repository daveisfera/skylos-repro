"""String-name type registry — only live reference to FacilityChoiceField."""

ANGULAR_TEMPLATES = {
    "CharField": {"type": "inline-input"},
    "ModelChoiceField": {"type": "select"},
    "FacilityChoiceField": {"type": "select"},
    "ChoiceField": {"type": "select"},
}


def form_field_type(field) -> str:
    try:
        return ANGULAR_TEMPLATES[field.__class__.__name__]["type"]
    except KeyError:
        return "select"
