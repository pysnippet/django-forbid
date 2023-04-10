from django.test import RequestFactory
from django.test import override_settings

from django_forbid.access import grants_access

factory = RequestFactory()
request = factory.get("/")
request.session = {}

LOCALHOST = "localhost"
IP_LOCAL1 = "0.0.0.0"
IP_LOCAL2 = "127.0.0.1"
IP_LONDON = "212.102.63.59"


def test_access_without_configuration():
    """If no configuration is provided, access is granted everywhere."""
    assert grants_access(request, LOCALHOST)


@override_settings(DJANGO_FORBID={"OPTIONS": {"VPN": True}})
def test_access_forbid_vpn():
    """If VPN detection is enabled, access is granted everywhere."""
    assert grants_access(request, LOCALHOST)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}}, DEBUG=True)
def test_access_from_localhost_development_mode():
    """In development mode, access is granted from localhost."""
    assert grants_access(request, IP_LOCAL1)
    assert grants_access(request, IP_LOCAL2)
    assert grants_access(request, LOCALHOST)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_localhost_production_mode():
    """In production mode, access is not granted from localhost."""
    assert not grants_access(request, IP_LOCAL1)
    assert not grants_access(request, IP_LOCAL2)
    assert not grants_access(request, LOCALHOST)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_in_countries_whitelist():
    """Access is granted from GB when GB is in the counties' whitelist."""
    assert grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_not_in_countries_whitelist():
    """Access is not granted from GB when GB is not in the counties' whitelist."""
    assert not grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["EU"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_eu_in_continent_whitelist():
    """Access is granted from GB when EU is in the continents' whitelist."""
    assert grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["US"], "OPTIONS": {"ACTION": "PERMIT"}})
def test_access_from_gb_when_gb_not_in_continent_whitelist():
    """Access is not granted from GB when EU is not in the continents' whitelist."""
    assert not grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_gb_in_forbidden_countries():
    """Access is not granted from GB when GB is in the forbidden list."""
    assert not grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["RU"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_gb_not_in_forbidden_countries():
    """Access is granted from GB when GB is not in the forbidden list."""
    assert grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["EU"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_eu_in_forbidden_territories():
    """Access is not granted from GB when EU is in the forbidden list."""
    assert not grants_access(request, IP_LONDON)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["AS"], "OPTIONS": {"ACTION": "FORBID"}})
def test_access_from_gb_when_eu_not_in_forbidden_territories():
    """Access is granted from GB when EU is not in the forbidden list."""
    assert grants_access(request, IP_LONDON)
