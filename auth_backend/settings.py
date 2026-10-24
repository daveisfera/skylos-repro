"""Settings wiring a duck-typed auth backend by dotted path (web-server shape)."""

INSTALLED_APPS = ["auth_backend"]
SECRET_KEY = "x"
ROOT_URLCONF = "auth_backend.urls"

AUTHENTICATION_BACKENDS = (
    "auth_backend.backends.MobileTokenBackend",
)
