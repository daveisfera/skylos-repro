"""Caller that uses get_hls_info — proves a cross-file live reference."""

from cross_file_miss.hls_helpers import get_hls_info


def describe(url: str) -> dict:
    return get_hls_info(url)


RESULT = describe("https://example.com/stream.m3u8")
