from .abstract_api import AbstractApi
from .const import Page, Selector, Zone


class ProtexialIOApi(AbstractApi):
    def __init__(self) -> None:
        self.pages = {
            Page.LOGIN: "/fr/login.htm",
            Page.LOGOUT: "/logout.htm",
            Page.PILOTAGE: "/fr/u_pilotage.htm",
            Page.STATUS: "/status.xml",
            Page.ERROR: "/fr/error.htm",
            Page.ELEMENTS: "/fr/u_plistelmt.htm",
            Page.CHALLENGE_CARD: "/fr/u_challenge.htm",
            Page.VERSION: "/cfg/vers",
            Page.DEFAULT: "/default.htm",
        }
        self.selectors = {
            Selector.CONTENT_TYPE: "meta[http-equiv='content-type']",
            Selector.LOGIN_CHALLENGE: "#form_id div:nth-child(6) b",
            Selector.ERROR_CODE: "#infobox b",
            Selector.FOOTER: "[id^='menu_footer']",
            Selector.CHALLENGE_CARD: "td:not([class])",
        }
        self.encoding = "utf-8"

    def get_login_payload(self, username, password, code):
        return {
            "login": username,
            "password": password,
            "key": code,
            "btn_login": "Se connecter",
        }

    def get_reset_session_payload(self):
        return {"btn_ok": "OK"}

    def get_arm_payload(self, zone):
        match zone:
            case Zone.A:
                return {"hidden": "hidden", "btn_zone_on_A": "Marche A"}
            case Zone.B:
                return {"hidden": "hidden", "btn_zone_on_B": "Marche B"}
            case Zone.C:
                return {"hidden": "hidden", "btn_zone_on_C": "Marche C"}
            case Zone.ABC:
                return {"hidden": "hidden", "btn_zone_on_ABC": "Marche A B C"}

    def get_disarm_payload(self):
        return {"hidden": "hidden", "btn_zone_off_ABC": "Arrêt A B C"}

    def get_turn_light_on_payload(self):
        return {"hidden": "hidden", "btn_lum_on": "ON"}

    def get_turn_light_off_payload(self):
        return {"hidden": "hidden", "btn_lum_off": "OFF"}

    def get_open_cover_payload(self):
        return {"hidden": "hidden", "btn_vol_up": ""}

    def get_close_cover_payload(self):
        return {"hidden": "hidden", "btn_vol_down": ""}

    def get_stop_cover_payload(self):
        return {"hidden": "hidden", "btn_vol_stop": "Stop"}
