"""Satellite logging settings — LOGGING lives here, imported into settings.py.

Mirrors pitchaware/settings_logging.py: dotted \"()\" paths are not in the
module that itself defines INSTALLED_APPS.
"""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "pa_extra": {
            "()": "logging_infra.json_formatter.ExtraAdder",
        },
    },
    "formatters": {
        "pa_json": {
            "()": "logging_infra.json_formatter.JSONFormatter",
        },
    },
    "handlers": {
        "pa_json": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["pa_extra"],
            "formatter": "pa_json",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["pa_json"],
        },
    },
}
