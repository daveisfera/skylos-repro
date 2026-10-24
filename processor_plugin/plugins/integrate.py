"""Bare processor class — product convention load, no static importers of the class."""


class IntegrateSessions:
    def __init__(self, session, debug=False, **kwargs):
        self.session = session
        self.debug = debug

    def process(self):
        return {"session": self.session, "integrated": True}
