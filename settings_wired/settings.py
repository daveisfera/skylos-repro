"""Recognizable Django settings wiring middleware and storage by dotted path."""

INSTALLED_APPS = ["settings_wired"]
SECRET_KEY = "x"
ROOT_URLCONF = "settings_wired.urls"

MIDDLEWARE = [
    "settings_wired.middleware.RouteMiddleware",
]

STORAGES = {
    "default": {
        "BACKEND": "settings_wired.storage.MediaStorage",
    },
}
