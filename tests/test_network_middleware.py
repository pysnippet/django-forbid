from django.test import RequestFactory
from django.test import override_settings

from django_forbid.skills.forbid_location import ForbidLocationMiddleware
from django_forbid.skills.forbid_network import ForbidNetworkMiddleware

LOCALHOST = "localhost"
IP_LONDON = "212.102.63.59"
IP_ZURICH = "146.70.99.178"


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


class SessionStore(dict):
    def has_key(self, key):
        return key in self


class WSGIRequest:
    def __init__(self, accept):
        self.accept = accept
        self.session = SessionStore()

    def get(self):
        request = RequestFactory().get("/")
        request.session = self.session
        request.META["HTTP_ACCEPT"] = self.accept
        return request

    def post(self, data):
        request = RequestFactory().post("/", data)
        request.session = self.session
        request.META["HTTP_ACCEPT"] = self.accept
        return request


class Detector:
    def __init__(self, get_response, ajax=False):
        access = "*/*" if ajax else "text/html"
        self.request = WSGIRequest(access)
        self.get_response = get_response

    def request_resource(self, ip_address=""):
        """Sends a request to the server to access a resource"""
        request = self.request.get()
        request.META["HTTP_X_FORWARDED_FOR"] = ip_address
        get_response = ForbidLocationMiddleware(self.get_response)
        return ForbidNetworkMiddleware(get_response)(request)

    def request_access(self):
        """Simulates the request sent by the user browser to the server"""
        request = self.request.post({"timezone": "Europe/London"})
        return ForbidNetworkMiddleware(self.get_response)(request)


def test_detect_no_config(get_response):
    """It should give access everyone when no config is provided"""
    assert skips(get_response, LOCALHOST)
    assert skips(get_response, IP_LONDON)
    assert skips(get_response, IP_ZURICH)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": False}})
def test_detect_when_vpn_disabled(get_response):
    """It should give access everyone when VPN is disabled"""
    assert skips(get_response, LOCALHOST)
    assert skips(get_response, IP_LONDON)
    assert skips(get_response, IP_ZURICH)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_detect_when_using_localhost(get_response):
    """It should give access to the user when using localhost"""
    assert not forbids(get_response, LOCALHOST)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_detect_when_using_nonlocal_ip(get_response):
    """User should pass through two requests to access the resource"""
    assert not forbids(get_response, IP_LONDON)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_detect_when_using_vpn(get_response):
    """User should be forbidden to access the resource when using VPN"""
    assert forbids(get_response, IP_ZURICH)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_detect_when_turns_off_vpn_after_using(get_response):
    """User should get access to the resource when VPN is turned off"""
    assert forbids(get_response, IP_ZURICH)

    # Turn off VPN - back to London
    assert not forbids(get_response, IP_LONDON)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_detect_when_using_ajax(get_response):
    """It should give access to the user when request is done by AJAX"""
    assert skips(get_response, LOCALHOST, True)
    assert skips(get_response, IP_LONDON, True)
