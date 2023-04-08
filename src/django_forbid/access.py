from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError


class Rule:
    # Key in the geoip2 city object.
    # Subclasses should override this.
    key = None

    def __init__(self, code):
        # Two-letter ISO 3166-1 alpha-2 code.
        self.code = code

    def __call__(self, city):
        """Checks if the code is satisfied."""
        return self.code == city.get(self.key)


class CountryRule(Rule):
    key = "country_code"


class ContinentRule(Rule):
    key = "continent_code"


class Access:
    # Variables in the settings module.
    # Subclasses should override this.
    countries = None
    territories = None

    # Hold the instance of GeoIP2.
    geoip = GeoIP2()

    def __init__(self):
        self.rules = []

        for country in getattr(settings, self.countries, []):
            self.rules.append(CountryRule(country.upper()))

        for territory in getattr(settings, self.territories, []):
            self.rules.append(ContinentRule(territory.upper()))

    def accessible(self, city):
        """Checks if the IP address is in the white zone."""
        return any(map(lambda rule: rule(city), self.rules))

    def grants(self, city):
        """Checks if the IP address is permitted."""
        raise NotImplementedError


class PermitAccess(Access):
    countries = "WHITELIST_COUNTRIES"
    territories = "WHITELIST_TERRITORIES"

    def grants(self, city):
        """Checks if the IP address is permitted."""
        return not self.rules or self.accessible(city)


class ForbidAccess(Access):
    countries = "FORBIDDEN_COUNTRIES"
    territories = "FORBIDDEN_TERRITORIES"

    def grants(self, city):
        """Checks if the IP address is forbidden."""
        return not self.rules or not self.accessible(city)


def grants_access(request, ip_address):
    """Checks if the IP address is in the white zone."""
    try:
        city = Access.geoip.city(ip_address)

        # Saves the timezone in the session for
        # comparing it with the timezone in the
        # POST request sent from user's browser
        # to detect if the user is using VPN.
        timezone = city.get("time_zone")
        request.session["tz"] = timezone

        # First, checks if the IP address is not
        # forbidden. If it is, False is returned
        # otherwise, checks if the IP address is
        # permitted.
        if ForbidAccess().grants(city):
            return PermitAccess().grants(city)
        return False
    except (AddressNotFoundError, Exception):
        # This happens when the IP address is not
        # in  the  GeoIP2 database. Usually, this
        # happens when the IP address is a local.
        return not any([
            ForbidAccess().rules,
            PermitAccess().rules,
        ]) or getattr(settings, "DEBUG", False)
