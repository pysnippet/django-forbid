import re

from device_detector import DeviceDetector

from .config import Settings


def detect_device(http_ua):
    device_aliases = {
        "portable media player": "player",
        "smart display": "display",
        "smart speaker": "speaker",
        "feature phone": "phone",
        "car browser": "car",
    }

    device_detector = DeviceDetector(http_ua)
    device_detector = device_detector.parse()
    device = device_detector.device_type()
    return device_aliases.get(device, device)


def normalize(device_type):
    """Removes the "!" prefix from the device type."""
    return device_type[1:]


def forbidden(device_type):
    """Checks if the device type is forbidden."""
    return device_type.startswith("!")


def permitted(device_type):
    """Checks if the device type is permitted."""
    return not forbidden(device_type)


def device_forbidden(device_type):
    devices = Settings.get("DEVICES", [])

    # Permit all devices if the
    # DEVICES setting is empty.
    if not devices:
        return False

    # Creates a regular expression in the following form:
    # ^(?=PERMITTED_DEVICES)(?:(?!FORBIDDEN_DEVICES)\w)+$
    # where the list of forbidden and permitted devices are
    # filtered from the DEVICES setting by the "!" prefix.
    permit = r"|".join(filter(permitted, devices))
    forbid = r"|".join(map(normalize, filter(forbidden, devices)))
    forbid = r"(?!" + forbid + r")" if forbid else ""
    regexp = r"^(?=" + permit + r")(?:" + forbid + r"\w)+$"

    # Regexp designed to match the permitted devices.
    # So, this checks if the device is not permitted.
    return not re.match(regexp, device_type)
