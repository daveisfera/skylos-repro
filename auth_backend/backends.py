"""Duck-typed auth backend — mirrors MobileTokenBackend (no ModelBackend/BaseBackend)."""


class MobileTokenBackend:
    """Wired only via AUTHENTICATION_BACKENDS; Django calls authenticate/get_user."""

    def authenticate(self, request, user_id=None, token=None):
        if not user_id or not token:
            return None
        return self.get_user(user_id)

    def get_user(self, user_id):
        return {"id": user_id}
