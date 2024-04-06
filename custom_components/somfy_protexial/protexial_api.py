from .abstract_api import AbstractApi
from .const import Page, Selector, Zone


class ProtexialApi(AbstractApi):
    def __init__(self) -> None:
        self.pages = {
            Page.LOGIN: "/fr/login.htm",
            Page.LOGOUT: "/logout.htm",
            Page.PILOTAGE: "/fr/u_pilotage.htm",
            Page.STATUS: "/status.xml",
            Page.ERROR: "/fr/error.htm",
            Page.ELEMENTS: "/fr/u_listelmt.htm",
            Page.CHALLENGE_CARD: "/fr/u_print.htm",
            Page.VERSION: "/cfg/vers",
            Page.DEFAULT: "/default.htm",
        }
        self.selectors = {
            Selector.CONTENT_TYPE: "meta[http-equiv='content-type']",
            Selector.LOGIN_CHALLENGE: "#form_id table tr:nth-child(4) td:nth-child(1) b",
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
            "btn_login": "Connexion",
        }

    def reset_session(self):
        return {"btn_ok": "OK"}

    def arm(self, zone):
        btnZone = ""
        match zone:
            case Zone.A:
                btnZone = "btn_zone_on_A"
            case Zone.B:
                btnZone = "btn_zone_on_B"
            case Zone.C:
                btnZone = "btn_zone_on_C"
            case Zone.ABC:
                btnZone = "btn_zone_on_ABC"

        return {"hidden": "hidden", btnZone: "Marche"}

    def disarm(self):
        return {"hidden": "hidden", "btn_zone_off_ABC": "Arrêt A B C"}

    def turn_light_on(self):
        return {"hidden": "hidden", "btn_lum_on": "ON"}

    def turn_light_off(self):
        return {"hidden": "hidden", "btn_lum_off": "OFF"}

    def open_cover(self):
        return {"hidden": "hidden", "btn_vol_up": ""}

    def close_cover(self):
        return {"hidden": "hidden", "btn_vol_down": ""}

    def stop_cover(self):
        return {"hidden": "hidden", "btn_vol_stop": ""}

    def reset_battery_status(self):
        return {"btn_del_pil": "Piles"}

    def reset_link_status(self):
        return {"btn_del_lia": "Liaisons"}

    def reset_alarm_status(self):
        return {"btn_del_alm": "Alarmes"}
