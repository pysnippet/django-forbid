import json
import re

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


def detect(get_response, request):
    response = get_response(request)

    # Checks if VPN detection is disabled
    # or if the `tz` session is not set.
    if any([
        # The session key is checked to avoid
        # redirect loops in development mode.
        not request.session.has_key("tz"),
        # Checks if FORBID_VPN is False or not set.
        not getattr(settings, "FORBID_VPN", False),
        # Checks if the request is an AJAX request.
        not re.search(
            r"\w+\/(?:html|xhtml\+xml|xml)",
            request.META.get("HTTP_ACCEPT"),
        ),
    ]):
        return response

    # Usually, this happens when CSRF is invalid.
    if response.status_code == 403:
        if hasattr(settings, "FORBIDDEN_URL"):
            return redirect(settings.FORBIDDEN_URL)
        return response

    if all(map(request.session.has_key, (
            "tz",
            "content",
            "charset",
            "headers",
            "status_code",
            "reason_phrase",
    ))) and request.POST.get("timezone", "N/A") == request.session.get("tz"):
        # Restores the response from the session.
        response = HttpResponse(
            content=request.session.get("content"),
            charset=request.session.get("charset"),
            status=request.session.get("status_code"),
            reason=request.session.get("reason_phrase"),
            headers=json.loads(request.session.get("headers")),
        )
        request.session.pop("content")
        request.session.pop("charset")
        request.session.pop("headers")
        request.session.pop("status_code")
        request.session.pop("reason_phrase")
        return response

    # Saves the response attributes in the session to restore it later.
    request.session["content"] = response.content.decode(response.charset)
    request.session["headers"] = json.dumps(dict(response.headers))
    request.session["charset"] = response.charset
    request.session["status_code"] = response.status_code
    request.session["reason_phrase"] = response.reason_phrase

    return render(request, "timezone.html", status=302)
