from django.test import override_settings
from django_forbid.middleware import ForbidMiddleware

from tests import IP, Header
from tests import WSGIRequest

wsgi = WSGIRequest()
request = wsgi.get()


def forbids(get_response, request):
    response = ForbidMiddleware(get_response)(request)
    if response.status_code == 302:
        request = wsgi.post({"timezone": "Europe/London"})
        response = ForbidMiddleware(get_response)(request)
    return response.status_code == 403


def test_should_allow_all_when_no_config_provided(get_response):
    """Should allow access to all users if no config is provided."""
    for ip_address in IP.all:
        request.META["HTTP_X_FORWARDED_FOR"] = ip_address
        assert not forbids(get_response, request)


@override_settings(DJANGO_FORBID={"DEVICES": ["desktop"]})
def test_should_allow_users_when_device_is_desktop(get_response):
    """Should allow access to desktop users only."""
    for user_agent in Header.all_user_agents:
        request.session["DEVICE"] = None
        request.META["HTTP_USER_AGENT"] = user_agent
        if user_agent != Header.user_agent_desktop:
            assert forbids(get_response, request)
            continue
        assert not forbids(get_response, request)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["NA"]})
def test_should_forbid_users_when_country_in_territories_blacklist(get_response):
    """Should forbid access to users from territories in blacklist."""
    for ip_address in IP.all:
        request.META["HTTP_X_FORWARDED_FOR"] = ip_address
        if ip_address in [*IP.locals, IP.ip_cobain]:
            assert forbids(get_response, request)
            continue
        assert not forbids(get_response, request)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"], "OPTIONS": {"ACTION": "PERMIT", "VPN": True}})
def test_should_allow_users_when_country_in_countries_whitelist(get_response):
    for ip_address in IP.all:
        request.META["HTTP_X_FORWARDED_FOR"] = ip_address
        if ip_address == IP.ip_london:
            assert not forbids(get_response, request)
            continue
        assert forbids(get_response, request)
