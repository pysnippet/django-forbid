from django.test import override_settings
from django_forbid.skills.forbid_device import ForbidDeviceMiddleware

from tests import Header
from tests import WSGIRequest

request = WSGIRequest().get()


def forbids(get_response, user_agent):
    request.session["DEVICE"] = None
    request.META["HTTP_USER_AGENT"] = user_agent
    response = ForbidDeviceMiddleware(get_response)(request)
    return response.status_code == 403


def test_should_allow_all_when_no_config_provided(get_response):
    """Should allow access to all_user_agents devices if no config is provided."""
    for user_agent in Header.all_user_agents:
        assert not forbids(get_response, user_agent)


@override_settings(DJANGO_FORBID={"DEVICES": []})
def test_should_allow_all_when_devices_are_empty(get_response):
    """Should allow access to all_user_agents devices if the list is empty, even if the user agent is unknown."""
    for user_agent in Header.all_user_agents:
        assert not forbids(get_response, user_agent)


@override_settings(DJANGO_FORBID={"DEVICES": ["desktop", "smartphone", "console", "tablet", "tv"]})
def test_should_allow_desktops_smartphones_consoles_tablets_and_tvs(get_response):
    """Should allow access to desktops, smartphones, consoles, tablets and TVs."""
    for user_agent in (Header.user_agent_peripheral, Header.user_agent_wearable, Header.user_agent_phablet,
                       Header.user_agent_display, Header.user_agent_speaker, Header.user_agent_camera,
                       Header.user_agent_player, Header.user_agent_phone, Header.user_agent_car,
                       Header.user_agent_unknown):
        assert forbids(get_response, user_agent)
    for user_agent in (Header.user_agent_desktop, Header.user_agent_smartphone, Header.user_agent_console,
                       Header.user_agent_tablet, Header.user_agent_tv):
        assert not forbids(get_response, user_agent)


@override_settings(DJANGO_FORBID={"DEVICES": ["!car", "!speaker", "!wearable"]})
def test_should_forbid_cars_speakers_and_wearables(get_response):
    """Should forbid access to cars, speakers and wearables."""
    for user_agent in (Header.user_agent_peripheral, Header.user_agent_smartphone, Header.user_agent_phablet,
                       Header.user_agent_desktop, Header.user_agent_console, Header.user_agent_display,
                       Header.user_agent_camera, Header.user_agent_tablet, Header.user_agent_player,
                       Header.user_agent_phone, Header.user_agent_tv):
        assert not forbids(get_response, user_agent)
    for user_agent in (Header.user_agent_car, Header.user_agent_speaker,
                       Header.user_agent_wearable, Header.user_agent_unknown):
        assert forbids(get_response, user_agent)


@override_settings(DJANGO_FORBID={"DEVICES": ["!phablet", "tablet", "phablet"]})
def test_should_forbid_device_when_sametime_permitted_and_forbidden(get_response):
    """Should forbid access if the same device is listed as permitted and forbidden."""
    for user_agent in (Header.user_agent_peripheral, Header.user_agent_smartphone, Header.user_agent_phablet,
                       Header.user_agent_desktop, Header.user_agent_console, Header.user_agent_display,
                       Header.user_agent_camera, Header.user_agent_player, Header.user_agent_phone,
                       Header.user_agent_tv, Header.user_agent_car, Header.user_agent_speaker,
                       Header.user_agent_wearable, Header.user_agent_unknown):
        assert forbids(get_response, user_agent)
    assert not forbids(get_response, Header.user_agent_tablet)


@override_settings(DJANGO_FORBID={"DEVICES": ["smartphone", "phablet", "tablet"]})
def test_should_forbid_unknown_devices_when_config_provided(get_response):
    """Should forbid access to unknown devices if the list of devices is not empty."""
    assert forbids(get_response, Header.user_agent_unknown)
