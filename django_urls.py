"""Minimal stand-in for django.urls.register_converter introspection."""


def register_converter(converter, name: str) -> None:
    _ = name
    _ = converter.regex
    converter.to_python("mg_1")
    converter.to_url(converter.to_python("mg_1"))
