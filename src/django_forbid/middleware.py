import re

from .skills.forbid_device import ForbidDeviceMiddleware
from .skills.forbid_location import ForbidLocationMiddleware
from .skills.forbid_network import ForbidNetworkMiddleware

__skills__ = (
    ForbidNetworkMiddleware,
    ForbidLocationMiddleware,
    ForbidDeviceMiddleware,
)


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.regex = re.compile(r"\w+/(?:html|xhtml\+xml|xml)")

    def __call__(self, request):
        get_response = self.get_response
        http_accept = request.META.get("HTTP_ACCEPT")
        if isinstance(http_accept, (bytes, str)) and self.regex.search(http_accept):
            for skill in __skills__:
                get_response = skill(get_response)
        return get_response(request)
