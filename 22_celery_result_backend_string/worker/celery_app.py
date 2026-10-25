from celery import Celery

app = Celery("worker")
app.conf.update(
    result_backend="worker.backends:ClusterResultBackend",
    task_serializer="json",
)
