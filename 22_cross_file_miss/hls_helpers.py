"""Cross-file helper — live when imported from hls_caller.py."""


def get_hls_info(url: str) -> dict:
    return {"url": url, "ok": True}
