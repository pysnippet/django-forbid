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

    def grants(self, ip_address):
        """Checks if the IP address is in the white zone."""
        city = self.geoip.city(ip_address)
        return any(map(lambda rule: rule(city), self.rules))


class PermitAccess(Access):
    countries = "WHITELIST_COUNTRIES"
    territories = "WHITELIST_TERRITORIES"

    def grants(self, ip_address):
        """Checks if the IP address is permitted."""
        try:
            return not self.rules or super().grants(ip_address)
        except AddressNotFoundError:
            return getattr(settings, "DEBUG", False)


class ForbidAccess(Access):
    countries = "FORBIDDEN_COUNTRIES"
    territories = "FORBIDDEN_TERRITORIES"

    def grants(self, ip_address):
        """Checks if the IP address is forbidden."""
        try:
            return not self.rules or not super().grants(ip_address)
        except AddressNotFoundError:
            return getattr(settings, "DEBUG", False)


def grants_access(ip_address):
    """Checks if the IP address is in the white zone."""
    if ForbidAccess().grants(ip_address):
        return PermitAccess().grants(ip_address)
    return False
