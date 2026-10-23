"""Storage backend — referenced only via STORAGES BACKEND string."""

from django.core.files.storage import Storage


class MediaStorage(Storage):
    def save(self, name, content, max_length=None):
        return name
