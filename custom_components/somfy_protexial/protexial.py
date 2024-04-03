import asyncio
from enum import Enum
import logging
import re
from urllib.parse import urlencode
from xml.etree import ElementTree as ET

from aiohttp import ClientError, ClientSession
from pyquery import PyQuery as pq

from .const import ApiType, Page, Selector
from .protexial_api import ProtexialApi
from .protexial_io_api import ProtexialIOApi
from .protexiom_api import ProtexiomApi

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
    gsm = "GSM connecté au réseau"
    recgsm = "4"
    opegsm = "Orange"
    camera = "Disabled"

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"zoneA:{self.zoneA}, zoneB:{self.zoneB}, zoneC:{self.zoneC}, battery:{self.battery}, radio:{self.radio}, door:{self.door}, alarm:{self.alarm}, box:{self.box}, gsm:{self.gsm}, recgsm:{self.recgsm}, opegsm:{self.opegsm}, camera:{self.camera}"


class Error(str, Enum):
    WRONG_CODE = "(0x0B00)"
    MAX_LOGIN_ATTEMPS = "(0x0904)"
    WRONG_CREDENTIALS = "(0x0812)"
    SESSION_ALREADY_OPEN = "(0x0902)"
    NOT_AUTHORIZED = "(0x0903)"
    UNKNOWN_PARAMETER = "(0x1003)"


TIMEOUT = 10


class SomfyProtexial:
    def __init__(
        self,
        session: ClientSession,
        url,
        api_type=None,
        username=None,
        password=None,
        codes=None,
    ) -> None:
        self.url = url
        self.api_type = api_type
        self.username = username
        self.password = password
        self.codes = codes
        self.session = session
        self.cookie = None
        self.api = self.load_api(self.api_type)

    async def __do_call(
        self,
        method,
        page,
        headers=None,
        data=None,
        retry=True,
        login=True,
        authenticated=True,
    ):
        if headers is None:
            headers = {}

        try:
            path = self.api.get_page(page)
            full_path = self.url + path
            if self.cookie and authenticated:
                headers["Cookie"] = self.cookie
            if data:
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            async with asyncio.timeout(TIMEOUT):
                _LOGGER.debug(f"Call to: {full_path}")
                if method == "get":
                    response = await self.session.get(full_path, headers=headers)
                elif method == "post":
                    encodedData = urlencode(data, encoding=self.api.get_encoding())
                    _LOGGER.debug(f"With payload: {data}")
                    _LOGGER.debug(f"With payload (encoded): {encodedData}")
                    response = await self.session.post(
                        self.url + path, data=encodedData, headers=headers
                    )
            _LOGGER.debug(f"Response path: {response.real_url.path}")
            _LOGGER.debug(f"Response headers: {response.headers}")
            _LOGGER.debug(
                f"Response body: {await response.text(self.api.get_encoding())}"
            )

            if response.status == 200:
                if (
                    response.real_url.path == self.api.get_page(Page.DEFAULT)
                    and retry is True
                ):
                    await self.__login()
                    return await self.__do_call(
                        method, page, headers, data, retry=False, login=False
                    )
                elif response.real_url.path == self.api.get_page(Page.ERROR):
                    dom = pq(await response.text(self.api.get_encoding()))
                    error_element = dom(self.api.get_selector(Selector.ERROR_CODE))
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
                            method, page, headers, data, retry=False, login=False
                        )
                    elif errorCode == Error.SESSION_ALREADY_OPEN:
                        if retry:
                            form = self.api.get_reset_session_payload()
                            await self.__do_call(
                                "post",
                                Page.ERROR,
                                data=form,
                                retry=False,
                            )
                            self.cookie = None
                            if login:
                                await self.__login()
                            return await self.__do_call(
                                method, page, headers, data, retry=False, login=login
                            )
                        else:
                            raise Exception("Too many login retries")
                    elif errorCode == Error.WRONG_CREDENTIALS:
                        raise Exception("Login failed: Wrong credentials")
                    elif errorCode == Error.MAX_LOGIN_ATTEMPS:
                        raise Exception("Login failed: Max attempt count reached")
                    elif errorCode == Error.WRONG_CODE:
                        raise Exception("Login failed: Wrong code")
                    elif errorCode == Error.UNKNOWN_PARAMETER:
                        raise Exception("Command failed: Unknown parameter")
                    else:
                        raise Exception(
                            f"Command failed: Unknown errorCode: {errorCode}"
                        )
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
                f"Timeout error fetching information from {full_path} - {exception}"
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
        version_string = "Unknown"
        try:
            error_response = await self.__do_call(
                "get", Page.LOGIN, login=False, authenticated=False
            )
            dom = pq(await error_response.text(self.api.get_encoding()))
            footer_element = dom(self.api.get_selector(Selector.FOOTER))
            if footer_element is not None:
                matches = re.search(
                    r"([0-9]{4}) somfy", footer_element.text(), re.IGNORECASE
                )
                if len(matches.groups()) > 0:
                    version_string = matches.group(1)

            if self.api.get_page(Page.VERSION) is not None:
                response = await self.__do_call(
                    "get", Page.VERSION, login=False, authenticated=False
                )
                version = await response.text(self.api.get_encoding())
                version_string += f" ({version.strip()})"
        except Exception as exception:
            _LOGGER.error("Failed to extract version: %s", exception)
        return version_string

    def load_api(self, type: ApiType):
        if type == ApiType.PROTEXIAL:
            return ProtexialApi()
        elif type == ApiType.PROTEXIAL_IO:
            return ProtexialIOApi()
        elif type == ApiType.PROTEXIOM:
            return ProtexiomApi()
        elif type is not None:
            raise Exception(f"Unknown api type: {type}")

    async def guess_and_set_api_type(self):
        for api_type in [ApiType.PROTEXIAL_IO, ApiType.PROTEXIAL, ApiType.PROTEXIOM]:
            self.api = self.load_api(api_type)
            has_version_page = False
            versionPage = self.api.get_page(Page.VERSION)
            if versionPage is not None:
                has_version_page = True
                version_body = await self.do_guess_get(versionPage)

            if not has_version_page or version_body is not None:
                loginPage = self.api.get_page(Page.LOGIN)
                login_body = await self.do_guess_get(loginPage)
                if login_body is not None:
                    dom = pq(login_body)
                    challenge_element = dom(
                        self.api.get_selector(Selector.LOGIN_CHALLENGE)
                    )
                    if challenge_element is not None:
                        self.api_type = api_type
                        return self.api_type
        raise Exception("Couldn't detect the centrale type")

    async def do_guess_get(self, page) -> str:
        try:
            async with asyncio.timeout(TIMEOUT):
                _LOGGER.debug(f"Guess {self.url + page}")
                response = await self.session.get(
                    self.url + page, headers={}, allow_redirects=False
                )
            if response.status == 200:
                response_body = await response.text(self.api.get_encoding())
                _LOGGER.debug(
                    f"Guess response: {await response.text(self.api.get_encoding())}"
                )
                return response_body
            # Looks like another model
        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                page,
                exception,
            )
            raise Exception(
                f"Timeout error fetching information from {page} - {exception}"
            )
        except ClientError as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                page,
                exception,
            )
            raise Exception(f"Error fetching information from {page} - {exception}")
        except Exception as exception:
            _LOGGER.error("Something really wrong happened! - %s", exception)
        return None

    async def get_challenge(self):
        login_response = await self.__do_call("get", Page.LOGIN, login=False)
        dom = pq(await login_response.text(self.api.get_encoding()))
        challenge_element = dom(self.api.get_selector(Selector.LOGIN_CHALLENGE))
        if challenge_element:
            return challenge_element.text()
        else:
            raise Exception("Challenge not found")

    async def __login(self, username=None, password=None, code=None):
        self.cookie = None
        if code is None:
            challenge = await self.get_challenge()
            code = self.codes[challenge]

        form = self.api.get_login_payload(
            username if username else self.username,
            password if password else self.password,
            code,
        )
        login_response = await self.__do_call(
            "post", Page.LOGIN, data=form, retry=False, login=False
        )
        self.cookie = login_response.headers.get("SET-COOKIE")

    async def logout(self):
        await self.__do_call("get", Page.LOGOUT, retry=False, login=False)
        self.cookie = None

    async def get_status(self):
        status_response = await self.__do_call(
            "get", Page.STATUS, login=False, authenticated=False
        )
        content = await status_response.text(self.api.get_encoding())
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
                case "gsm":
                    status.gsm = child.text
                case "recgsm":
                    status.recgsm = child.text
                case "opegsm":
                    status.opegsm = child.text
                case "camera":
                    status.camera = child.text
        return status

    async def get_challenge_card(self, username, password, code):
        await self.__login(username, password, code)
        status_response = await self.__do_call("get", Page.CHALLENGE_CARD, login=False)
        dom = pq(await status_response.text(self.api.get_encoding()))
        all_challenge_elements = dom(self.api.get_selector(Selector.CHALLENGE_CARD))
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
        form = self.api.get_arm_payload(zone)
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def disarm(self):
        form = self.api.get_disarm_payload()
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def turn_light_on(self):
        form = self.api.get_turn_light_on_payload()
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def turn_light_off(self):
        form = self.api.get_turn_light_off_payload()
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def open_cover(self):
        form = self.api.get_open_cover_payload()
        await self.__do_call("post", Page.PILOTAGE, data=form)

    async def close_cover(self):
        form = self.api.get_close_cover_payload()
        response = await self.__do_call("post", Page.PILOTAGE, data=form)
        print(await response.text(self.api.get_encoding()))

    async def stop_cover(self):
        form = self.api.get_stop_cover_payload()
        await self.__do_call("post", Page.PILOTAGE, data=form)
