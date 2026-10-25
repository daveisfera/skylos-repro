class ClusterResultBackend:
    """Loaded only via Celery result_backend string (colon path)."""

    def get(self, key):
        return None
