"""Settings fragment wiring the formatter by dotted path only."""

LOGGING = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "18_logging_infra.json_formatter.JSONFormatter",
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
