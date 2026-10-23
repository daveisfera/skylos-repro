"""Convention loader matching Skylos importlib_plugins fixture shape."""

from importlib import import_module

PLUGIN_MODULE = "processor_plugin.plugins.integrate"


def load_processor(name=PLUGIN_MODULE):
    module = import_module(name)
    return module.IntegrateSessions


def run(payload: dict) -> dict:
    cls = load_processor()
    return cls().process(payload)


RESULT = run({"ok": True})
