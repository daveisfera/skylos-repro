"""Settings fragment wiring the auth backend by dotted path only."""

AUTHENTICATION_BACKENDS = [
    "12_auth_backend.backends.TokenAuthBackend",
]
