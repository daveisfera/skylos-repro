"""Recognizable Django settings wiring the formatter by dotted path only."""

INSTALLED_APPS = ["logging_infra"]
SECRET_KEY = "x"
ROOT_URLCONF = "logging_infra.urls"

LOGGING = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "logging_infra.json_formatter.JSONFormatter",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
