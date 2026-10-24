"""Convention loader: processor path chosen by name string only.

No module-level RESULT= that proves IntegrateSessions live — the class is only
reachable when a runtime name selects the dotted path (web-server style).
"""

from importlib import import_module

# Registry of logical name → module path (class name is conventional).
PROCESSORS = {
    "integrate_sessions": "processor_plugin.plugins.integrate",
}


def load_processor(name: str):
    module_path = PROCESSORS[name]
    module = import_module(module_path)
    return getattr(module, "IntegrateSessions")


def run_named(name: str, session):
    cls = load_processor(name)
    return cls(session).process()
