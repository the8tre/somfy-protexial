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
            Page.ELEMENTS: "/fr/u_listelmt.htm",
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

    def login(self, username, password, code):
        return {
            "login": username,
            "password": password,
            "key": code,
            "btn_login": "Se connecter",
        }

    def reset_session(self):
        return {"btn_ok": "OK"}

    def arm(self, zone):
        match zone:
            case Zone.A:
                return {"hidden": "hidden", "btn_zone_on_A": "Marche A"}
            case Zone.B:
                return {"hidden": "hidden", "btn_zone_on_B": "Marche B"}
            case Zone.C:
                return {"hidden": "hidden", "btn_zone_on_C": "Marche C"}
            case Zone.ABC:
                return {"hidden": "hidden", "btn_zone_on_ABC": "Marche A B C"}

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
        return {"hidden": "hidden", "btn_vol_stop": "Stop"}

    def reset_battery_status(self):
        return {"btn_del_pil": "Piles"}

    def reset_link_status(self):
        return {"btn_del_lia": "Liaisons"}

    def reset_alarm_status(self):
        return {"btn_del_alm": "Alarmes"}