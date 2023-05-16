from django.test import RequestFactory
from django.test import override_settings

from django_forbid.skills.forbid_device import ForbidDeviceMiddleware

unknown_ua = "curl/7.47.0"
peripheral_ua = "Mozilla/5.0 (Linux; Android 7.0; SHTRIH-SMARTPOS-F2 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.91 Mobile Safari/537.36"
smartphone_ua = "SAMSUNG-GT-S3850/S3850CXKD1 SHP/VPP/R5 Dolfin/2.0 NexPlayer/3.0 SMM-MMS/1.2.0 profile/MIDP-2.1 configuration/CLDC-1.1 OPN-B"
wearable_ua = "Mozilla/5.0 (Linux; Android 8.1.0; KidPhone4G Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.125 Mobile Safari/537.36"
phablet_ua = "Mozilla/5.0 (Linux; Android 6.0; GI-626 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
desktop_ua = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.28) Gecko/20130316 Songbird/1.12.1 (20140112193149)"
console_ua = "Mozilla/5.0 (Linux; Android 4.1.1; ARCHOS GAMEPAD Build/JRO03H) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"
display_ua = "Mozilla/5.0 (Linux; U; Android 4.0.4; fr-be; DA220HQL Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
speaker_ua = "AlexaMediaPlayer/2.0.201528.0 (Linux;Android 5.1.1) ExoPlayerLib/1.5.9"
camera_ua = "Mozilla/5.0 (Linux; U; Android 2.3.3; ja-jp; COOLPIX S800c Build/CP01_WW) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
tablet_ua = "Mozilla/5.0 (iPad3,6; iPad; U; CPU OS 7_1 like Mac OS X; en_US) com.google.GooglePlus/33839 (KHTML, like Gecko) Mobile/P103AP (gzip)"
player_ua = "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8C148"
phone_ua = "lephone K10/Dorado WAP-Browser/1.0.0"
car_ua = "Mozilla/5.0 (Linux; Android 4.4.2; CarPad-II-P Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
tv_ua = "Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager"

factory = RequestFactory()
request = factory.get("/")
request.session = {}


def forbids(get_response, user_agent):
    request.session["DEVICE"] = None
    request.META["HTTP_USER_AGENT"] = user_agent
    response = ForbidDeviceMiddleware(get_response)(request)
    return response.status_code == 403


def test_access_with_empty_list_of_devices(get_response):
    """Should allow access to all devices if no config is provided."""
    for device_ua in (peripheral_ua, smartphone_ua, wearable_ua, phablet_ua,
                      desktop_ua, console_ua, display_ua, speaker_ua, camera_ua,
                      tablet_ua, player_ua, phone_ua, car_ua, tv_ua, unknown_ua):
        assert not forbids(get_response, device_ua)


@override_settings(DJANGO_FORBID={"DEVICES": []})
def test_access_with_empty_list_of_devices(get_response):
    """Should allow access to all devices if the list is empty, even if the user agent is unknown."""
    for device_ua in (peripheral_ua, smartphone_ua, wearable_ua, phablet_ua,
                      desktop_ua, console_ua, display_ua, speaker_ua, camera_ua,
                      tablet_ua, player_ua, phone_ua, car_ua, tv_ua, unknown_ua):
        assert not forbids(get_response, device_ua)


@override_settings(DJANGO_FORBID={"DEVICES": ["desktop", "smartphone", "console", "tablet", "tv"]})
def test_access_desktops_smartphones_consoles_tablets_and_tvs(get_response):
    """Should allow access to desktops, smartphones, consoles, tablets and TVs."""
    for device_ua in (peripheral_ua, wearable_ua, phablet_ua, display_ua,
                      speaker_ua, camera_ua, player_ua, phone_ua, car_ua, unknown_ua):
        assert forbids(get_response, device_ua)
    for device_ua in (desktop_ua, smartphone_ua, console_ua, tablet_ua, tv_ua):
        assert not forbids(get_response, device_ua)


@override_settings(DJANGO_FORBID={"DEVICES": ["!car", "!speaker", "!wearable"]})
def test_forbid_access_to_cars_speakers_and_wearables(get_response):
    """Should forbid access to cars, speakers and wearables."""
    for device_ua in (peripheral_ua, smartphone_ua, phablet_ua, desktop_ua, console_ua,
                      display_ua, camera_ua, tablet_ua, player_ua, phone_ua, tv_ua):
        assert not forbids(get_response, device_ua)
    for device_ua in (car_ua, speaker_ua, wearable_ua, unknown_ua):
        assert forbids(get_response, device_ua)


@override_settings(DJANGO_FORBID={"DEVICES": ["!phablet", "tablet", "phablet"]})
def test_forbid_access_if_same_device_is_listed_as_permitted_and_forbidden(get_response):
    """Should forbid access if the same device is listed as permitted and forbidden."""
    for device_ua in (peripheral_ua, smartphone_ua, phablet_ua, desktop_ua,
                      console_ua, display_ua, camera_ua, player_ua, phone_ua,
                      tv_ua, car_ua, speaker_ua, wearable_ua, unknown_ua):
        assert forbids(get_response, device_ua)
    assert not forbids(get_response, tablet_ua)


@override_settings(DJANGO_FORBID={"DEVICES": ["smartphone", "phablet", "tablet"]})
def test_forbid_access_unknown_devices_if_devices_are_set(get_response):
    """Should forbid access to unknown devices if the list of devices is not empty."""
    assert forbids(get_response, unknown_ua)
