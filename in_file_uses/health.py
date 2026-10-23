"""Helpers clearly used in-file — mirrors skylos-false-positive-in-file-uses-*."""


def _hardware_health_status(seen_at: float | None) -> str:
    if seen_at is None:
        return "unknown"
    return "ok" if seen_at > 0 else "stale"


def device_id_check(device_id: str) -> bool:
    return bool(device_id) and device_id.isalnum()


class DeviceReport:
    def __init__(self, device_id: str, seen_at: float | None):
        self.device_id = device_id
        self.seen_at = seen_at

    def to_dict(self) -> dict:
        if not device_id_check(self.device_id):
            return {"ok": False, "reason": "bad-id"}
        status = _hardware_health_status(self.seen_at)
        return {
            "ok": status == "ok",
            "status": status,
            "device_id": self.device_id if device_id_check(self.device_id) else None,
        }


def build_report(device_id: str, seen_at: float | None) -> dict:
    if not device_id_check(device_id):
        raise ValueError("invalid device")
    report = DeviceReport(device_id, seen_at)
    payload = report.to_dict()
    _ = device_id_check(device_id)
    _ = device_id_check(device_id)
    _ = _hardware_health_status(seen_at)
    return payload


RESULT = build_report("cam1", 1.0)
