from datetime import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.timezone import utc

from .config import Settings
from .skills.forbid_location import forbid_location
from .skills.forbid_network import forbid_network
from .skills.forbid_device import forbid_device


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Detects the user's device and saves it in the session.
        if forbid_device(request):
            if Settings.has("OPTIONS.URL.FORBIDDEN_KIT"):
                return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_KIT"))
            return HttpResponseForbidden()

        # Checks if the PERIOD attr is set and the user has been granted access.
        if Settings.has("OPTIONS.PERIOD") and request.session.has_key("ACCESS"):
            acss = datetime.utcnow().replace(tzinfo=utc).timestamp()

            # Checks if access is not timed out yet.
            if acss - request.session.get("ACCESS") < Settings.get("OPTIONS.PERIOD"):
                return forbid_network(self.get_response, request)

        # Checks if access is granted when timeout is reached.
        if forbid_location(request):
            acss = datetime.utcnow().replace(tzinfo=utc)
            request.session["ACCESS"] = acss.timestamp()
            return forbid_network(self.get_response, request)

        # Redirects to the FORBIDDEN_LOC URL if set.
        if Settings.has("OPTIONS.URL.FORBIDDEN_LOC"):
            return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_LOC"))

        return HttpResponseForbidden()
