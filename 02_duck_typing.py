"""Duck typing: external library calls a method on a passed-in client."""


class Boto3Client:
    # m3u8.load() calls http_client.download() — no static reference in this repo.
    @staticmethod
    def download(uri, *_) -> tuple[str, str]:
        bucket, key = uri[5:].split("/", 1)
        return f"{bucket}/{key}", ""


def load_m3u8_from_s3(uri: str):
    # Stand-in for m3u8.load(uri, http_client=...); lives in an external package.
    from external_m3u8 import load as m3u8_load

    return m3u8_load(uri, http_client=Boto3Client())
