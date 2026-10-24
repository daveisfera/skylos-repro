"""Storage backend referenced only via STORAGES BACKEND string."""


class MediaStorage:
    def save(self, name, content, max_length=None):
        return name
