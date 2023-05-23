import re

from device_detector import DeviceDetector
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from . import Settings


def normalize(device_type):
    """Removes the "!" prefix from the device type."""
    return device_type[1:]


def forbidden(device_type):
    """Checks if the device type is forbidden."""
    return device_type.startswith("!")


def permitted(device_type):
    """Checks if the device type is permitted."""
    return not forbidden(device_type)


class ForbidDeviceMiddleware:
    """Checks if the user device is forbidden."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_aliases = {
            "portable media player": "player",
            "smart display": "display",
            "smart speaker": "speaker",
            "feature phone": "phone",
            "car browser": "car",
        }

        device_type = request.session.get("DEVICE")
        devices = Settings.get("DEVICES", [])

        # Permit all devices if the
        # DEVICES setting is empty.
        if not devices:
            return self.get_response(request)

        if not request.session.get("DEVICE"):
            http_ua = request.META.get("HTTP_USER_AGENT")
            device_detector = DeviceDetector(http_ua)
            device_detector = device_detector.parse()
            device = device_detector.device_type()
            device_type = device_aliases.get(device, device)
            request.session["DEVICE"] = device_type

        # Creates a regular expression in the following form:
        # ^(?=PERMITTED_DEVICES)(?:(?!FORBIDDEN_DEVICES)\w)+$
        # where the list of forbidden and permitted devices are
        # filtered from the DEVICES setting by the "!" prefix.
        permit = r"|".join(filter(permitted, devices))
        forbid = r"|".join(map(normalize, filter(forbidden, devices)))
        forbid = r"(?!" + forbid + r")" if forbid else ""
        regexp = r"^(?=" + permit + r")(?:" + forbid + r"\w)+$"

        # Regexp designed to match the permitted devices.
        if re.match(regexp, device_type):
            return self.get_response(request)

        # Redirects to the FORBIDDEN_KIT URL if set.
        if Settings.has("OPTIONS.URL.FORBIDDEN_KIT"):
            return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_KIT"))

        return HttpResponseForbidden()
