from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .access import AccessFactory


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        address = request.META.get("REMOTE_ADDR")
        address = request.META.get("HTTP_X_FORWARDED_FOR", address)
        ip = address.split(",")[0].strip()

        if AccessFactory.get_access().is_granted(ip):
            return self.get_response(request)

        # Redirect to forbidden page if defined else return 403
        if hasattr(settings, "FORBIDDEN_URL"):
            return redirect(getattr(settings, "FORBIDDEN_URL"))

        return HttpResponseForbidden()
