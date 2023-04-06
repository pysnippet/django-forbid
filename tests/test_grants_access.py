from django.test import RequestFactory
from django.test import override_settings

from django_forbid.access import grants_access

factory = RequestFactory()
request = factory.get("/")
request.session = {}


def test_access_without_configuration():
    """If no configuration is provided, access is granted everywhere."""
    assert grants_access(request, "doesnt-matter")


@override_settings(WHITELIST_COUNTRIES=["US"], DEBUG=True)
def test_access_from_localhost_development_mode():
    """In development mode, access is granted from localhost."""
    assert grants_access(request, "127.0.0.1")
    assert grants_access(request, "localhost")


@override_settings(WHITELIST_COUNTRIES=["US"])
def test_access_from_localhost_production_mode():
    """In production mode, access is not granted from localhost."""
    assert not grants_access(request, "127.0.0.1")
    assert not grants_access(request, "localhost")


@override_settings(WHITELIST_COUNTRIES=["GB"])
def test_access_from_gb_when_gb_in_countries_whitelist():
    """Access is granted from GB when GB is in the counties' whitelist."""
    assert grants_access(request, "212.102.63.59")


@override_settings(WHITELIST_COUNTRIES=["US"])
def test_access_from_gb_when_gb_not_in_countries_whitelist():
    """Access is not granted from GB when GB is not in the counties' whitelist."""
    assert not grants_access(request, "212.102.63.59")


@override_settings(WHITELIST_TERRITORIES=["EU"])
def test_access_from_gb_when_eu_in_continent_whitelist():
    """Access is granted from GB when EU is in the continents' whitelist."""
    assert grants_access(request, "212.102.63.59")


@override_settings(WHITELIST_TERRITORIES=["US"])
def test_access_from_gb_when_gb_not_in_continent_whitelist():
    """Access is not granted from GB when EU is not in the continents' whitelist."""
    assert not grants_access(request, "212.102.63.59")


@override_settings(FORBIDDEN_COUNTRIES=["GB"])
def test_access_from_gb_when_gb_in_forbidden_countries():
    """Access is not granted from GB when GB is in the forbidden list."""
    assert not grants_access(request, "212.102.63.59")


@override_settings(FORBIDDEN_COUNTRIES=["RU"])
def test_access_from_gb_when_gb_not_in_forbidden_countries():
    """Access is granted from GB when GB is not in the forbidden list."""
    assert grants_access(request, "212.102.63.59")


@override_settings(FORBIDDEN_TERRITORIES=["EU"])
def test_access_from_gb_when_eu_in_forbidden_territories():
    """Access is not granted from GB when EU is in the forbidden list."""
    assert not grants_access(request, "212.102.63.59")


@override_settings(FORBIDDEN_TERRITORIES=["AS"])
def test_access_from_gb_when_eu_not_in_forbidden_territories():
    """Access is granted from GB when EU is not in the forbidden list."""
    assert grants_access(request, "212.102.63.59")


@override_settings(WHITELIST_TERRITORIES=["EU"], FORBIDDEN_COUNTRIES=["GB"])
def test_mix_config_access_from_gb_when_eu_in_whitelist_but_gb_is_forbidden():
    """Access is not granted from GB when EU is in the whitelist but GB is forbidden."""
    assert not grants_access(request, "212.102.63.59")


@override_settings(WHITELIST_COUNTRIES=["GB"], FORBIDDEN_COUNTRIES=["GB"])
def test_mix_config_access_from_gb_when_gb_in_both_lists():
    """Access is not granted from GB when GB is in both lists."""
    assert not grants_access(request, "212.102.63.59")
