from datetime import datetime

from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.timezone import utc

from .access import grants_access


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        address = request.META.get("REMOTE_ADDR")
        address = request.META.get("HTTP_X_FORWARDED_FOR", address)

        # Checks if the timeout variable is set and the user has been granted access.
        if hasattr(settings, "FORBID_TIMEOUT") and request.session.has_key("ACCESS"):
            acss = datetime.utcnow().replace(tzinfo=utc).timestamp()

            # Checks if access is not timed out yet.
            if acss - request.session.get("ACCESS") < settings.FORBID_TIMEOUT:
                return self.get_response(request)

        # Checks if access is granted when timeout is reached.
        if grants_access(address.split(",")[0].strip()):
            acss = datetime.utcnow().replace(tzinfo=utc)
            request.session["ACCESS"] = acss.timestamp()
            return self.get_response(request)

        # Redirects to forbidden page if URL is set.
        if hasattr(settings, "FORBIDDEN_URL"):
            return redirect(settings.FORBIDDEN_URL)

        return HttpResponseForbidden()
