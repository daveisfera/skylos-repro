"""Settings fragment wiring middleware and storage by dotted path only."""

MIDDLEWARE = [
    "13_settings_middleware_storage.middleware.RouteMiddleware",
]

DEFAULT_FILE_STORAGE = "13_settings_middleware_storage.storage.MediaStorage"
