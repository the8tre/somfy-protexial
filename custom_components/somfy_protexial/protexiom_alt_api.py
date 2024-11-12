from .abstract_api import AbstractApi
from .const import Page, Selector, Zone


class ProtexiomAltApi(AbstractApi):
    def __init__(self) -> None:
        self.pages = {
            Page.LOGIN: "/login.htm",
            Page.LOGOUT: "/logout.htm",
            Page.PILOTAGE: "/u_pilotage.htm",
            Page.STATUS: "/status.xml",
            Page.ERROR: "/error.htm",
            Page.ELEMENTS: "/u_plistelmt.htm",
            Page.CHALLENGE_CARD: "/u_print.htm",
            Page.VERSION: None,
            Page.DEFAULT: "/default.htm",
        }
        self.selectors = {
            Selector.CONTENT_TYPE: "meta[http-equiv='content-type']",
            Selector.LOGIN_CHALLENGE: "#form_id table tr:nth-child(3) td:nth-child(1)",
            Selector.ERROR_CODE: "#infobox b",
            Selector.FOOTER: "[id^='menu_footer']",
            Selector.CHALLENGE_CARD: "td:not([class])",
        }
        self.encoding = "iso-8859-15"

    def get_login_payload(self, username, password, code):
        return {
            "login": username,
            "password": password,
            "key": code,
            "action": "Connexion",
        }

    def get_reset_session_payload(self):
        return {"action": "OK"}

    def get_arm_payload(self, zone):
        value = ""
        match zone:
            case Zone.A:
                value = "Marche A"
            case Zone.B:
                value = "Marche B"
            case Zone.C:
                value = "Marche C"
            case Zone.ABC:
                value = "Marche A B C"

        return {"hidden": "hidden", "zone": value}

    def get_disarm_payload(self):
        return {"hidden": "hidden", "zone": "Arrêt A B C"}

    def get_turn_light_on_payload(self):
        return {"hidden": "hidden", "action_lum": "ON"}

    def get_turn_light_off_payload(self):
        return {"hidden": "hidden", "action_lum": "OFF"}

    def get_open_cover_payload(self):
        return {"hidden": "hidden", "action_vol_montee": ""}

    def get_close_cover_payload(self):
        return {"hidden": "hidden", "action_vol_descente": ""}

    def get_stop_cover_payload(self):
        return {"hidden": "hidden", "action_vol_stop": ""}
