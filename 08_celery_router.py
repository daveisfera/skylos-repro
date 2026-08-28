"""Celery task router — referenced from app config by dotted path string."""


def route_task(name, args, kwargs, options, task=None, **kw):
    if name == "celery.chord_unlock" and options:
        if queue := options.get("queue"):
            return {"queue": queue}
    return None


class Celery:
    def __init__(self):
        # Same contract as Celery(task_routes=("08_celery_router.route_task",)).
        self.task_routes = ("08_celery_router.route_task",)


app = Celery()
