"""Handlers registered in a name→callable map and invoked by string key."""


def reboot(device_id: str) -> dict:
    return {"action": "reboot", "device_id": device_id}


def ping(device_id: str) -> dict:
    return {"action": "ping", "device_id": device_id}


COMMANDS = {
    "reboot": reboot,
    "ping": ping,
}


def dispatch(name: str, device_id: str) -> dict:
    handler = COMMANDS[name]
    return handler(device_id)
