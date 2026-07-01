"""Minimal stand-in for the third-party m3u8 package's duck-typed client protocol."""


def load(uri: str, http_client) -> tuple[str, str]:
    return http_client.download(uri)
