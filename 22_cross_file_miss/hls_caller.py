"""Caller that uses get_hls_info — proves a cross-file live reference."""

from hls_helpers import get_hls_info


def describe(url: str) -> dict:
    return get_hls_info(url)
