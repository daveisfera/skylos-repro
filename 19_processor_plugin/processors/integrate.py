"""Processor plugin — loaded by name string, not a static import."""


class IntegrateSessions:
    name = "integrate_sessions"

    def process(self, payload: dict) -> dict:
        return {**payload, "integrated": True}
