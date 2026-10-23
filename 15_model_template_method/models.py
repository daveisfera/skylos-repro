"""Model method used from a Django template, not from Python call sites."""


class Record:
    def __init__(self, name: str):
        self.name = name

    def get_display_name(self) -> str:
        return self.name.upper()
