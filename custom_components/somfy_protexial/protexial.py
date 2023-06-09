import asyncio
from enum import Enum
import logging
from xml.etree import ElementTree as ET

from aiohttp import ClientError, ClientSession
import async_timeout
from pyquery import PyQuery as pq

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Status:
    zoneA = "off"
    zoneB = "off"
    zoneC = "off"
    battery = "ok"
    radio = "ok"
    door = "ok"
    alarm = "ok"
    box = "ok"

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"zoneA:{self.zoneA}, zoneB:{self.zoneB}, zoneC:{self.zoneC}, battery:{self.battery}, radio:{self.radio}, door:{self.door}, alarm:{self.alarm}, box:{self.box}"


class Page(str, Enum):
    LOGIN = "/fr/login.htm"
    LOGOUT = "/logout.htm"
    PILOTAGE = "/fr/u_pilotage.htm"
    STATUS = "/status.xml"
    ERROR = "/fr/error.htm"
    ELEMENTS = "/fr/u_plistelmt.htm"
    PRINT = "/fr/u_print.htm"
    VERSION = "/cfg/vers"
    DEFAULT = "/default.htm"


class Selector(str, Enum):
    CHALLENGE_ELEMENT = "#form_id table tr:nth-child(4) td:nth-child(1) b"
    ERROR_ELEMENT = "#infobox b"
    CHALLENGE_ELEMENT_LIST = "td:not([class])"


class Error(str, Enum):
    WRONG_CODE = "(0x0B00)"
    MAX_LOGIN_ATTEMPS = "(0x0904)"
    WRONG_CREDENTIALS = "(0x0812)"
    SESSION_ALREADY_OPEN = "(0x0902)"
    NOT_AUTHORIZED = "(0x0903)"


class Zone(Enum):
    A = 0
    B = 1
    C = 2
    ABC = 3


TIMEOUT = 10


class SomfyProtexial:
    def __init__(
        self, session: ClientSession, url, username=None, password=None, codes=None
    ):
        self.url = url
        self.username = username
        self.password = password
        self.codes = codes
        self.session = session
        self.cookie = None

    async def __do_call(
        self, method, path, headers={}, data=None, retry=True, login=True
    ):
        try:
            if self.cookie:
                headers["Cookie"] = self.cookie
            if data:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self.session.get(self.url + path, headers=headers)
                elif method == "post":
                    response = await self.session.post(
                        self.url + path, data=data, headers=headers
                    )

            if response.status == 200:
                if response.real_url.path == Page.DEFAULT and retry is True:
                    await self.__login()
                    return await self.__do_call(
                        method, path, headers, data, retry=False, login=False
                    )
                elif response.real_url.path == Page.ERROR:
                    dom = pq(await response.text())
                    error_element = dom(Selector.ERROR_ELEMENT)
                    if not error_element:
                        raise Exception("Unknown error")
                    errorCode = error_element.text()
                    if (
                        errorCode == Error.NOT_AUTHORIZED
                        and not self.cookie
                        and retry is True
                    ):
                        await self.__login()
                        return await self.__do_call(
                            method, path, headers, data, retry=False, login=False
                        )
                    elif errorCode == Error.SESSION_ALREADY_OPEN:
                        if retry:
                            form = {"btn_ok": "OK"}
                            await self.__do_call(
                                "post",
                                Page.ERROR,
                                form,
                                retry=False,
                            )
                            self.cookie = None
                            if login:
                                await self.__login()
                            return await self.__do_call(
                                method, path, headers, data, retry=False, login=login
                            )
                        else:
                            raise Exception("Too many login retries")
                    elif errorCode == Error.WRONG_CREDENTIALS:
                        raise Exception("Login failed: Wrong credentials")
                    elif errorCode == Error.MAX_LOGIN_ATTEMPS:
                        raise Exception("Login failed: Max attempt count reached")
                    elif errorCode == Error.WRONG_CODE:
                        raise Exception("Login failed: Wrong code")
                    else:
                        raise Exception("Login failed: Unknown error")
                else:
                    return response
            else:
                raise Exception(f"Http error ({response.status})")
        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                path,
                exception,
            )
            raise Exception(
                f"Timeout error fetching information from {path} - {exception}"
            )

        except ClientError as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                path,
                exception,
            )
            raise Exception(f"Error fetching information from {path} - {exception}")
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
            raise Exception(f"Something really wrong happened! - {exception}")

    async def init(self):
        await self.__login()

    async def get_version(self):
        response = await self.__do_call("get", Page.VERSION, login=False)
        return await response.text()

    async def get_challenge(self):
        login_response = await self.__do_call("get", Page.LOGIN, login=False)
        dom = pq(await login_response.text())
        challenge_element = dom(Selector.CHALLENGE_ELEMENT)
        if challenge_element:
            return challenge_element.text()
        else:
            raise Exception("Challenge not found")

    async def __login(self, username=None, password=None, code=None):
        self.cookie = None
        if code is None:
            challenge = await self.get_challenge()
            code = self.codes[challenge]

        form = {
            "login": username if username else self.username,
            "password": password if password else self.password,
            "key": code,
            "btn_login": "Connexion",
        }
        login_response = await self.__do_call(
            "post", Page.LOGIN, data=form, retry=False, login=False
        )
        self.cookie = login_response.headers.get("SET-COOKIE")

    async def logout(self):
        await self.__do_call("get", Page.LOGOUT, retry=False, login=False)
        self.cookie = None

    async def get_status(self):
        status_response = await self.__do_call("get", Page.STATUS)
        content = await status_response.text()
        response = ET.fromstring(content)
        status = Status()
        for child in response:
            match child.tag:
                case "defaut0":
                    status.battery = child.text
                case "defaut1":
                    status.radio = child.text
                case "defaut2":
                    status.door = child.text
                case "defaut3":
                    status.alarm = child.text
                case "defaut4":
                    status.box = child.text
                case "zone0":
                    status.zoneA = child.text
                case "zone1":
                    status.zoneB = child.text
                case "zone2":
                    status.zoneC = child.text
        return status

    async def get_challenge_card(self, username, password, code):
        await self.__login(username, password, code)
        status_response = await self.__do_call("get", Page.PRINT, login=False)
        dom = pq(await status_response.text())
        all_challenge_elements = dom(Selector.CHALLENGE_ELEMENT_LIST)
        challenges = {}
        chars = ["A", "B", "C", "D", "E", "F"]
        global_index = 0
        row_index = 0
        col_index = 0
        for elmt in all_challenge_elements:
            col_index = global_index % 6
            if col_index == 0:
                row_index = row_index + 1
            challenges[f"{chars[col_index]}{row_index}"] = elmt.text
            global_index = global_index + 1
        await self.logout()
        return challenges

    async def arm(self, zone):
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

        form = {"hidden": "hidden", btnZone: "Marche"}
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def disarm(self):
        form = {"hidden": "hidden", "btn_zone_off_ABC": "Arret"}
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def turn_light_on(self):
        form = {"hidden": "hidden", "btn_lum_on": "ON"}
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def turn_light_off(self):
        form = {"hidden": "hidden", "btn_lum_off": "OFF"}
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def open_cover(self):
        form = {"hidden": "hidden", "btn_vol_up": ""}
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def close_cover(self):
        form = {"hidden": "hidden", "btn_vol_down": ""}
        response = await self.__do_call("post", Page.PILOTAGE, data=form)
        print(await response.text())

    async def stop_cover(self):
        form = {"hidden": "hidden", "btn_vol_stop": ""}
        await self.__do_call("post", Page.PILOTAGE, data=form)
