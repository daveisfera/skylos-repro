"""Celery-like conf using colon result_backend path (not AUTHENTICATION_BACKENDS)."""


class Celery:
    def __init__(self):
        # Same contract as Celery(result_backend="pkg.mod:ClassName").
        self.result_backend = (
            "celery_result_backend.backend:RedisClusterBackend"
        )


app = Celery()
