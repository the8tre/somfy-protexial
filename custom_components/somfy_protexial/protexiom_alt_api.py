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
            Page.ELEMENTS: "/u_listelmt.htm",
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

    def login(self, username, password, code):
        return {
            "login": username,
            "password": password,
            "key": code,
            "action": "Connexion",
        }

    def reset_session(self):
        return {"action": "OK"}

    def arm(self, zone):
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

    def disarm(self):
        return {"hidden": "hidden", "zone": "Arrêt A B C"}

    def turn_light_on(self):
        return {"hidden": "hidden", "action_lum": "ON"}

    def turn_light_off(self):
        return {"hidden": "hidden", "action_lum": "OFF"}

    def open_cover(self):
        return {"hidden": "hidden", "action_vol_montee": ""}

    def close_cover(self):
        return {"hidden": "hidden", "action_vol_descente": ""}

    def stop_cover(self):
        return {"hidden": "hidden", "action_vol_stop": ""}

    def reset_battery_status(self):
        return {"btn_del_pil": "Piles"}

    def reset_link_status(self):
        return {"btn_del_lia": "Liaisons"}

    def reset_alarm_status(self):
        return {"btn_del_alm": "Alarmes"}
