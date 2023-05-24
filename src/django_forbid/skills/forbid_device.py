from device_detector import DeviceDetector
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from . import Access
from . import Settings


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

        devices = Settings.get("DEVICES", [])
        device_type = request.session.get("DEVICE")

        # Skip if DEVICES empty.
        if not devices:
            return self.get_response(request)

        if not device_type:
            http_ua = request.META.get("HTTP_USER_AGENT")
            device_detector = DeviceDetector(http_ua)
            device_detector = device_detector.parse()
            device = device_detector.device_type()
            device_type = device_aliases.get(device, device)
            request.session["DEVICE"] = device_type

        if Access(devices).grants(device_type):
            return self.get_response(request)

        # Redirects to the FORBIDDEN_DEV URL if set.
        if Settings.has("OPTIONS.URL.FORBIDDEN_DEV"):
            return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_DEV"))

        return HttpResponseForbidden()
