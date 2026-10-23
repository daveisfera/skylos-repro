"""Logging formatter — referenced only via LOGGING dict dotted path."""

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
