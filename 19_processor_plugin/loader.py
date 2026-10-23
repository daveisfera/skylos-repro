"""Convention loader: import module + getattr by configured name."""

import importlib


PROCESSOR_PATH = "19_processor_plugin.processors.integrate"
PROCESSOR_CLASS = "IntegrateSessions"


def load_processor():
    module = importlib.import_module(PROCESSOR_PATH)
    cls = getattr(module, PROCESSOR_CLASS)
    return cls()


def run(payload: dict) -> dict:
    return load_processor().process(payload)
