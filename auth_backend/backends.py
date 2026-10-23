"""Authentication backend — referenced only via AUTHENTICATION_BACKENDS string."""


class TokenAuthBackend:
    """Django looks this up by dotted path from settings."""

    def authenticate(self, request, token=None, **kwargs):
        if token == "ok":
            return object()
        return None

    def get_user(self, user_id):
        return None


class StaleAuthBackend:
    """Intentionally unused — should still be reported."""

    def authenticate(self, request, **kwargs):
        return None
