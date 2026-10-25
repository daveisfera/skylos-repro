"""Schema handlers — only reached via factory getattr(form_schemas, name)."""


def get_game_form_schema(request):
    return {"fields": []}
