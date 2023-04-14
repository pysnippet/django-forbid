from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

from .config import Settings


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
    countries = "COUNTRIES"
    territories = "TERRITORIES"

    # Hold the instance of GeoIP2.
    geoip = GeoIP2()

    def __init__(self):
        self.rules = []

        if Settings.has(self.countries):
            for country in Settings.get(self.countries):
                self.rules.append(CountryRule(country.upper()))

        if Settings.has(self.territories):
            for territory in Settings.get(self.territories):
                self.rules.append(ContinentRule(territory.upper()))

    def accessible(self, city):
        """Checks if the IP address is in the white zone."""
        return any(map(lambda rule: rule(city), self.rules))

    def grants(self, city):
        """Checks if the IP address is permitted."""
        raise NotImplementedError


class PermitAccess(Access):
    def grants(self, city):
        """Checks if the IP address is permitted."""
        return not self.rules or self.accessible(city)


class ForbidAccess(Access):
    def grants(self, city):
        """Checks if the IP address is forbidden."""
        return not self.rules or not self.accessible(city)


class Factory:
    """Creates an instance of the Access class."""

    FORBID = ForbidAccess
    PERMIT = PermitAccess

    @classmethod
    def create_access(cls, action):
        return getattr(cls, action)()


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

        # Creates an instance of the Access class
        # and checks if the IP address is granted.
        action = Settings.get("OPTIONS.ACTION", "FORBID")
        return Factory.create_access(action).grants(city)
    except (AddressNotFoundError, Exception):
        # This happens when the IP address is not
        # in  the  GeoIP2 database. Usually, this
        # happens when the IP address is a local.
        return not any([
            Settings.has(Access.countries),
            Settings.has(Access.territories),
        ]) or getattr(settings, "DEBUG", False)
