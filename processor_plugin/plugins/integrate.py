"""Processor plugin — loaded by name string via importlib."""


class IntegrateSessions:
    name = "integrate_sessions"

    def process(self, payload: dict) -> dict:
        return {**payload, "integrated": True}


def unused_plugin_hook():
    return "unused"
