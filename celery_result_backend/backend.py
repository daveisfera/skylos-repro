"""Celery result backend class — only referenced via module:Class string."""


class RedisClusterBackend:
    """Wired as result_backend=\"celery_result_backend.backend:RedisClusterBackend\"."""

    def __init__(self, app=None, url=None, **kwargs):
        self.app = app
        self.url = url
