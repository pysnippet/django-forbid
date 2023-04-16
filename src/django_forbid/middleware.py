from datetime import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.timezone import utc

from .access import grants_access
from .config import Settings
from .detect import detect_vpn
from .device import detect_device
from .device import device_forbidden


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        address = request.META.get("REMOTE_ADDR")
        address = request.META.get("HTTP_X_FORWARDED_FOR", address)

        # Detects the user's device and saves it in the session.
        if not request.session.get("DEVICE"):
            http_ua = request.META.get("HTTP_USER_AGENT")
            request.session["DEVICE"] = detect_device(http_ua)

        if device_forbidden(request.session.get("DEVICE")):
            if Settings.has("OPTIONS.URL.FORBIDDEN_KIT"):
                return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_KIT"))
            return HttpResponseForbidden()

        # Checks if the PERIOD attr is set and the user has been granted access.
        if Settings.has("OPTIONS.PERIOD") and request.session.has_key("ACCESS"):
            acss = datetime.utcnow().replace(tzinfo=utc).timestamp()

            # Checks if access is not timed out yet.
            if acss - request.session.get("ACCESS") < Settings.get("OPTIONS.PERIOD"):
                return detect_vpn(self.get_response, request)

        # Checks if access is granted when timeout is reached.
        if grants_access(request, address.split(",")[0].strip()):
            acss = datetime.utcnow().replace(tzinfo=utc)
            request.session["ACCESS"] = acss.timestamp()
            return detect_vpn(self.get_response, request)

        # Redirects to the FORBIDDEN_LOC URL if set.
        if Settings.has("OPTIONS.URL.FORBIDDEN_LOC"):
            return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_LOC"))

        return HttpResponseForbidden()
