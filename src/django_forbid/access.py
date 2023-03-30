from pathlib import Path

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError


class Rule:
    # key in the geoip2 city object
    # subclasses should override this
    key = None

    def __init__(self, code):
        # two-letter ISO 3166-1 alpha-2 code
        self.code = code

    def __call__(self, city):
        """Check if the code is satisfied."""
        return self.code == city.get(self.key)


class CountryRule(Rule):
    key = "country_code"


class ContinentRule(Rule):
    key = "continent_code"


class Access:
    # variables in the settings module
    # subclasses should override this
    countries = None
    territories = None

    def __init__(self):
        self.rules = []
        self.geoip = GeoIP2(Path(__file__).resolve().parent / "geoip")

        for country in getattr(settings, self.countries, []):
            self.rules.append(CountryRule(country.upper()))

        for territory in getattr(settings, self.territories, []):
            self.rules.append(ContinentRule(territory.upper()))

    def is_granted(self, ip_address):
        """Check if the IP address is in the access zone."""
        city = self.geoip.city(ip_address)
        return any(map(lambda rule: rule(city), self.rules))


class PermitAccess(Access):
    countries = "WHITELIST_COUNTRIES"
    territories = "WHITELIST_TERRITORIES"

    def is_granted(self, ip_address):
        """Check if the IP address is permitted."""
        try:
            return super().is_granted(ip_address)
        except AddressNotFoundError:
            return False


class ForbidAccess(Access):
    countries = "FORBIDDEN_COUNTRIES"
    territories = "FORBIDDEN_TERRITORIES"

    def is_granted(self, ip_address):
        """Check if the IP address is forbidden."""
        try:
            return not super().is_granted(ip_address)
        except AddressNotFoundError:
            return False


class AccessFactory:
    permit = PermitAccess
    forbid = ForbidAccess

    class PermitAll:
        @staticmethod
        def is_granted(_):
            return True

    @classmethod
    def get_access(cls):
        """Return the access object based on the settings."""

        if hasattr(settings, cls.forbid.countries) or hasattr(settings, cls.forbid.territories):
            return cls.forbid()

        if hasattr(settings, cls.permit.countries) or hasattr(settings, cls.permit.territories):
            return cls.permit()

        # if no settings are provided, permit all
        return cls.PermitAll()
