"""getattr via nested registry method name — closer to api/lovable/factory.py."""

from registry_getattr import handlers, registry


def dispatch(kind: str, request):
    spec = registry.HANDLERS[kind]
    return getattr(handlers, spec["method"])(request)
