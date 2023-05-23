from django.test import override_settings
from django_forbid.skills.forbid_location import ForbidLocationMiddleware
from django_forbid.skills.forbid_network import ForbidNetworkMiddleware

from tests import IP
from tests import WSGIRequest


def skips(get_response, ip_address, ajax=False):
    detector = Detector(get_response, ajax=ajax)
    response = detector.request_resource(ip_address)
    return response.status_code == 200


def forbids(get_response, ip_address):
    detector = Detector(get_response)
    response = detector.request_resource(ip_address)
    assert response.status_code == 302
    response = detector.request_access()
    return response.status_code == 403


class Detector:
    def __init__(self, get_response, ajax=False):
        self.request = WSGIRequest(ajax)
        self.get_response = get_response

    def request_resource(self, ip_address=""):
        """Sends a request to the server to access a resource"""
        request = self.request.get()
        request.META["HTTP_X_FORWARDED_FOR"] = ip_address
        get_response = ForbidLocationMiddleware(self.get_response)
        return ForbidNetworkMiddleware(get_response)(request)

    def request_access(self):
        """Simulates the request sent by the user browser to the server"""
        request = self.request.post({"CLIENT_TZ": "Europe/London"})
        return ForbidNetworkMiddleware(self.get_response)(request)


def test_should_allow_all_when_no_config_provided(get_response):
    """It should give access everyone when no config is provided"""
    for ip_address in IP.all:
        assert skips(get_response, ip_address)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": False}})
def test_should_allow_all_when_vpn_disabled(get_response):
    """It should give access everyone when VPN is disabled"""
    for ip_address in IP.all:
        assert skips(get_response, ip_address)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_should_allow_users_only_from_great_britain(get_response):
    """It should give access to the user from Great Britain"""
    for ip_address in IP.locals:
        assert not forbids(get_response, ip_address)
    assert not forbids(get_response, IP.ip_london)
    assert forbids(get_response, IP.ip_zurich)
    assert forbids(get_response, IP.ip_cobain)
    # Turn off VPN - back to London
    assert not forbids(get_response, IP.ip_london)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_should_allow_ajax_requests(get_response):
    """It should give access to the user when request is done by AJAX"""
    for ip_address in IP.all:
        assert skips(get_response, ip_address, True)
