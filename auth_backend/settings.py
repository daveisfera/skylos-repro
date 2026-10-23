"""Recognizable Django settings module wiring the auth backend by dotted path."""

INSTALLED_APPS = ["auth_backend"]
SECRET_KEY = "x"
ROOT_URLCONF = "auth_backend.urls"

AUTHENTICATION_BACKENDS = [
    "auth_backend.backends.TokenAuthBackend",
]
