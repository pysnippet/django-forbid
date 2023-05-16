from django.test import RequestFactory


class IP:
    localhost = "localhost"
    ip_local1 = "0.0.0.0"
    ip_local2 = "127.0.0.1"
    ip_london = "212.102.63.59"
    ip_zurich = "146.70.99.178"
    ip_cobain = "104.129.57.189"

    locals = [
        localhost,
        ip_local1,
        ip_local2,
    ]

    all = [
        *locals,
        ip_london,
        ip_zurich,
        ip_cobain,
    ]


class Header:
    accept_html = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    accept_json = "application/json"

    user_agent_unknown = "curl/7.47.0"
    user_agent_peripheral = (
        "Mozilla/5.0 (Linux; Android 7.0; SHTRIH-SMARTPOS-F2 Build/NRD90M; wv) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.91 Mobile Safari/537.36"
    )
    user_agent_smartphone = (
        "SAMSUNG-GT-S3850/S3850CXKD1 SHP/VPP/R5 Dolfin/2.0 NexPlayer"
        "/3.0 SMM-MMS/1.2.0 profile/MIDP-2.1 configuration/CLDC-1.1 OPN-B"
    )
    user_agent_wearable = (
        "Mozilla/5.0 (Linux; Android 8.1.0; KidPhone4G Build/O11019; wv) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.125 Mobile Safari/537.36"
    )
    user_agent_phablet = (
        "Mozilla/5.0 (Linux; Android 6.0; GI-626 Build/MRA58K) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Chrome/53.0.2785.124 Mobile Safari/537.36"
    )
    user_agent_desktop = (
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.28) Gecko/20130316 Songbird/1.12.1 (20140112193149)"
    )
    user_agent_console = (
        "Mozilla/5.0 (Linux; Android 4.1.1; ARCHOS GAMEPAD Build/JRO03H) "
        "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"
    )
    user_agent_display = (
        "Mozilla/5.0 (Linux; U; Android 4.0.4; fr-be; DA220HQL Build/IMM76D) "
        "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
    )
    user_agent_speaker = (
        "AlexaMediaPlayer/2.0.201528.0 (Linux;Android 5.1.1) ExoPlayerLib/1.5.9"
    )
    user_agent_camera = (
        "Mozilla/5.0 (Linux; U; Android 2.3.3; ja-jp; COOLPIX S800c Build/CP01_WW) "
        "AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    )
    user_agent_tablet = (
        "Mozilla/5.0 (iPad3,6; iPad; U; CPU OS 7_1 like Mac OS X; en_US) "
        "com.google.GooglePlus/33839 (KHTML, like Gecko) Mobile/P103AP (gzip)"
    )
    user_agent_player = (
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; ja-jp) "
        "AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8C148"
    )
    user_agent_phone = "lephone K10/Dorado WAP-Browser/1.0.0"
    user_agent_car = (
        "Mozilla/5.0 (Linux; Android 4.4.2; CarPad-II-P Build/KOT49H) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36"
    )
    user_agent_tv = (
        "Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager"
    )

    all_user_agents = (
        user_agent_peripheral, user_agent_smartphone, user_agent_wearable, user_agent_phablet, user_agent_desktop,
        user_agent_console, user_agent_display, user_agent_speaker, user_agent_camera, user_agent_tablet,
        user_agent_player, user_agent_phone, user_agent_car, user_agent_tv, user_agent_unknown,
    )


class SessionStore(dict):
    def has_key(self, key):
        return key in self


class WSGIRequest:
    def __init__(self, ajax=False):
        self.session = SessionStore()
        if ajax:
            self.accept = Header.accept_json
        else:
            self.accept = Header.accept_html

    def get(self):
        request = RequestFactory().get("/")
        request.session = self.session
        request.META["HTTP_ACCEPT"] = self.accept
        return request

    def post(self, data):
        request = RequestFactory().post("/", data)
        request.session = self.session
        request.META["HTTP_ACCEPT"] = self.accept
        return request
