import json

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render

from . import Settings


class ForbidNetworkMiddleware:
    """Checks if the user network is forbidden."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response_attributes = ("content", "charset", "status", "reason")

        def erase_response_attributes():
            for attr in response_attributes:
                request.session.pop(attr)

        def forbidden_page():
            # Redirects to the FORBIDDEN_NET URL if set.
            if Settings.has("OPTIONS.URL.FORBIDDEN_NET"):
                return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_NET"))
            return HttpResponseForbidden()

        geoip2_tz = request.session.get("GEOIP2_TZ")
        verified_tz = request.session.get("VERIFIED_TZ", "")

        # Checks if the user's timezone match with the last accessed one.
        if verified_tz == geoip2_tz or not Settings.get("OPTIONS.VPN", False):
            return self.get_response(request)
        # Checks if GEOIP2_TZ and VERIFIED_TZ don't exist.
        elif verified_tz and geoip2_tz != "N/A":
            return forbidden_page()

        if all(map(request.session.has_key, ("GEOIP2_TZ", *response_attributes))):
            # Handles if the user's timezone differs from the
            # one determined by GeoIP API. If so, VPN is used.
            client_tz = request.POST.get("CLIENT_TZ", verified_tz)

            if geoip2_tz != "N/A" and client_tz != geoip2_tz:
                request.session["VERIFIED_TZ"] = ""
                erase_response_attributes()
                return forbidden_page()

            # Restores the response from the session.
            response = HttpResponse(**{
                attr: request.session.get(attr) for attr in response_attributes
            })
            if hasattr(response, "headers"):
                response.headers = json.loads(request.session.get("headers"))
            request.session["VERIFIED_TZ"] = geoip2_tz
            erase_response_attributes()
            return response

        # Gets the response and saves attributes in the session to restore it later.
        response = self.get_response(request)
        if hasattr(response, "headers"):
            # In older versions of Django, HttpResponse does not have headers.
            request.session["headers"] = json.dumps(dict(response.headers))
        request.session["content"] = response.content.decode(response.charset)
        request.session["charset"] = response.charset
        request.session["status"] = response.status_code
        request.session["reason"] = response.reason_phrase

        return render(request, "timezone.html", status=302)
