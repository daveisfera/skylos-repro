"""Handlers only reached via getattr(handlers, HANDLERS[kind])."""


def create_item(request):
    return {"ok": True, "request": request}


def get_item_schema(request):
    return {"fields": [], "request": request}


def unused_mutation():
    return "stale"
