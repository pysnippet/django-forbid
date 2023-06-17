import itertools

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from geoip2.errors import AddressNotFoundError

from . import Access
from . import Settings
from . import continents_codes


class ForbidLocationMiddleware:
    """Checks if the user location is forbidden."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        city = dict()
        geoip = GeoIP2()
        address = request.META.get("REMOTE_ADDR")
        address = request.META.get("HTTP_X_FORWARDED_FOR", address)
        client_ip = address.split(",")[0].strip()
        verified_ip = request.session.get("VERIFIED_IP", "")

        if verified_ip and verified_ip == client_ip:
            return self.get_response(request)

        try:
            city = geoip.city(client_ip)

            countries = Settings.get("COUNTRIES", [])
            territories = Settings.get("TERRITORIES", [])
            country_state_code = city.get("region")
            country_identifier = city.get("country_code")

            if territories:
                # Adds the continent codes of the countries that are forbidden partially.
                territories = list({*territories, *itertools.chain.from_iterable(
                    map(continents_codes.__getitem__, filter(bool, map(Access.getattr, countries)))
                )})

            if country_state_code:
                country_identifier += ":%s" % country_state_code
            granted = all([
                Access(countries).grants(country_identifier),
                Access(territories).grants(city.get("continent_code")),
            ])
        except (AddressNotFoundError, Exception):
            # This happens when the IP address is not
            # in  the  GeoIP2 database. Usually, this
            # happens when the IP address is a local.
            granted = not any([
                Settings.has("COUNTRIES"),
                Settings.has("TERRITORIES"),
            ]) or getattr(settings, "DEBUG", False)
        finally:
            # Saves the timezone in the session for
            # comparing it with the timezone in the
            # POST request sent from user's browser
            # to detect if the user is using a VPN.
            timezone = city.get("time_zone", "N/A")
            request.session["GEOIP2_TZ"] = timezone

        if granted:
            request.session["VERIFIED_IP"] = client_ip
            return self.get_response(request)

        # Erases the timezone from the session.
        request.session["VERIFIED_IP"] = ""

        # Redirects to the FORBIDDEN_LOC URL if set.
        if Settings.has("OPTIONS.URL.FORBIDDEN_LOC"):
            return redirect(Settings.get("OPTIONS.URL.FORBIDDEN_LOC"))

        return HttpResponseForbidden()
