from django.test import override_settings
from django_forbid.skills.forbid_location import ForbidLocationMiddleware

from tests import IP
from tests import WSGIRequest

request = WSGIRequest().get()


def forbids(get_response, ip_address):
    request.META["HTTP_X_FORWARDED_FOR"] = ip_address
    response = ForbidLocationMiddleware(get_response)(request)
    return response.status_code == 403


def test_should_allow_all_when_no_config_provided(get_response):
    """If no configuration is provided, access is granted everywhere."""
    for ip_address in IP.all:
        assert not forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"]}, DEBUG=True)
def test_should_allow_all_when_development_mode(get_response):
    """In development mode, access is granted from localhost."""
    for ip_address in IP.locals:
        assert not forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US"]})
def test_should_forbid_all_when_production_mode(get_response):
    """In production mode, access is not granted from localhost."""
    for ip_address in IP.locals:
        assert forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["US:WA"]})
def test_should_allow_users_only_from_washington(get_response):
    """Access is granted from Washington."""
    for ip_address in IP.all:
        if ip_address != IP.ip_cobain:
            assert forbids(get_response, ip_address)
            continue
        assert not forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["!US:TX"]})
def test_should_forbid_users_only_from_texas(get_response):
    """Access is forbidden from Texas."""
    for ip_address in IP.all:
        if ip_address in [*IP.locals, IP.ip_dallas]:
            assert forbids(get_response, ip_address)
            continue
        assert not forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["!US:TX", "!US:IL", "GB"], "TERRITORIES": ["EU"]})
def test_should_forbid_users_only_from_texas_and_illinois(get_response):
    """Access is forbidden from Texas and Illinois."""
    for ip_address in IP.all:
        if ip_address in [*IP.locals, IP.ip_dallas]:
            assert forbids(get_response, ip_address)
            continue
        assert not forbids(get_response, ip_address)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["GB"]})
def test_should_allow_country_when_country_in_countries_whitelist_otherwise_forbid(get_response):
    """Access is granted from GB when GB is in the counties' whitelist."""
    assert not forbids(get_response, IP.ip_london)
    assert forbids(get_response, IP.ip_zurich)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["EU"]})
def test_should_allow_country_when_country_in_territories_whitelist_otherwise_forbid(get_response):
    """Access is granted from GB when EU is in the continents' whitelist."""
    assert not forbids(get_response, IP.ip_london)
    assert forbids(get_response, IP.ip_cobain)


@override_settings(DJANGO_FORBID={"COUNTRIES": ["!GB"]})
def test_should_forbid_country_when_country_in_countries_blacklist_otherwise_allow(get_response):
    """Access is not granted from GB when GB is in the forbidden list."""
    assert forbids(get_response, IP.ip_london)
    assert not forbids(get_response, IP.ip_cobain)


@override_settings(DJANGO_FORBID={"TERRITORIES": ["!EU"]})
def test_should_forbid_country_when_country_in_territories_blacklist_otherwise_allow(get_response):
    """Access is not granted from GB when EU is in the forbidden list."""
    assert forbids(get_response, IP.ip_london)
    assert not forbids(get_response, IP.ip_cobain)
