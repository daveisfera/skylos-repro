"""Storage backend — referenced only via DEFAULT_FILE_STORAGE string."""


class MediaStorage:
    def save(self, name, content):
        return name
