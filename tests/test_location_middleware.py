from django.test import RequestFactory
from django.test import override_settings

from django_forbid.skills.forbid_location import ForbidLocationMiddleware

factory = RequestFactory()
request = factory.get("/")
request.session = {}

LOCALHOST = "localhost"
IP_LOCAL1 = "0.0.0.0"
IP_LOCAL2 = "127.0.0.1"
IP_LONDON = "212.102.63.59"


def get_status_code(get_response, ip_address):
    request.META["HTTP_X_FORWARDED_FOR"] = ip_address
    response = ForbidLocationMiddleware(get_response)(request)
    return response.status_code


def test_access_without_configuration(get_response):
    """If no configuration is provided, access is granted everywhere."""
    assert get_status_code(get_response, LOCALHOST) == 200


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_access_forbid_vpn(get_response):
    """If VPN detection is enabled, access is granted everywhere."""
    assert get_status_code(get_response, LOCALHOST) == 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}}, DEBUG=True)
def test_access_from_localhost_development_mode(get_response):
    """In development mode, access is granted from localhost."""
    assert get_status_code(get_response, IP_LOCAL1) == 200
    assert get_status_code(get_response, IP_LOCAL2) == 200
    assert get_status_code(get_response, LOCALHOST) == 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_localhost_production_mode(get_response):
    """In production mode, access is not granted from localhost."""
    assert get_status_code(get_response, IP_LOCAL1) != 200
    assert get_status_code(get_response, IP_LOCAL2) != 200
    assert get_status_code(get_response, LOCALHOST) != 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_in_countries_whitelist(get_response):
    """Access is granted from GB when GB is in the counties' whitelist."""
    assert get_status_code(get_response, IP_LONDON) == 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_not_in_countries_whitelist(get_response):
    """Access is not granted from GB when GB is not in the counties' whitelist."""
    assert get_status_code(get_response, IP_LONDON) != 200


@override_settings(DJANGO_FORBID={"TERRITORIES": ["EU"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_eu_in_continent_whitelist(get_response):
    """Access is granted from GB when EU is in the continents' whitelist."""
    assert get_status_code(get_response, IP_LONDON) == 200


@override_settings(DJANGO_FORBID={"TERRITORIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_not_in_continent_whitelist(get_response):
    """Access is not granted from GB when EU is not in the continents' whitelist."""
    assert get_status_code(get_response, IP_LONDON) != 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_gb_in_forbidden_countries(get_response):
    """Access is not granted from GB when GB is in the forbidden list."""
    assert get_status_code(get_response, IP_LONDON) != 200


@override_settings(DJANGO_FORBID={"COUNTRIES": ["RU"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_gb_not_in_forbidden_countries(get_response):
    """Access is granted from GB when GB is not in the forbidden list."""
    assert get_status_code(get_response, IP_LONDON) == 200


@override_settings(DJANGO_FORBID={"TERRITORIES": ["EU"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_eu_in_forbidden_territories(get_response):
    """Access is not granted from GB when EU is in the forbidden list."""
    assert get_status_code(get_response, IP_LONDON) != 200


@override_settings(DJANGO_FORBID={"TERRITORIES": ["AS"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_eu_not_in_forbidden_territories(get_response):
    """Access is granted from GB when EU is not in the forbidden list."""
    assert get_status_code(get_response, IP_LONDON) == 200
