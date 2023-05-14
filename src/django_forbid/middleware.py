from .skills.forbid_device import ForbidDeviceMiddleware
from .skills.forbid_location import ForbidLocationMiddleware
from .skills.forbid_network import ForbidNetworkMiddleware

__skills__ = (
    ForbidDeviceMiddleware,
    ForbidLocationMiddleware,
    ForbidNetworkMiddleware,
)


class ForbidMiddleware:
    """Middleware to forbid access to the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for skill in __skills__:
            self.get_response = skill(self.get_response)
        return self.get_response(request)
