"""Logging formatter — only named from settings_logging LOGGING["()"] strings."""

import json
import logging


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "level": record.levelname,
                "msg": record.getMessage(),
                "name": record.name,
            }
        )


class ExtraAdder:
    """Filter constructed via LOGGING filters \"()\" path — web-server pa_extra shape."""

    def filter(self, record: logging.LogRecord) -> bool:
        return True
