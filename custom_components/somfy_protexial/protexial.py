import asyncio
import logging
import re
import string
from urllib.parse import urlencode
from xml.etree import ElementTree as ET

from aiohttp import ClientError, ClientSession
from pyquery import PyQuery as pq

from custom_components.somfy_protexial.retryable_somfy_exception import (
    RetryableSomfyException,
)

from .const import CHALLENGE_REGEX, HTTP_TIMEOUT, ApiType, Page, Selector, SomfyError
from .protexial_api import ProtexialApi
from .protexial_io_api import ProtexialIOApi
from .protexiom_api import ProtexiomApi
from .somfy_exception import SomfyException

_LOGGER: logging.Logger = logging.getLogger(__name__)

_PRINTABLE_CHARS = set(string.printable)


class Status:
    zoneA = None  # on | off
    zoneB = None  # on | off
    zoneC = None  # on | off
    battery = None  # ok | nok
    radio = None  # ok | nok
    door = None  # ok | nok
    alarm = None  # ok | nok
    box = None  # ok | nok
    gsm = None  # gsm connect au rseau | module gsm absent
    recgsm = None  # 0-n | missing
    opegsm = None  # - | orange | sfr | bouygues | free ...
    camera = None  # disabled | enabled
    error_count = 0

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"zoneA:{self.zoneA}, zoneB:{self.zoneB}, zoneC:{self.zoneC}, battery:{self.battery}, radio:{self.radio}, door:{self.door}, alarm:{self.alarm}, box:{self.box}, gsm:{self.gsm}, recgsm:{self.recgsm}, opegsm:{self.opegsm}, camera:{self.camera}"


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

            response = None
            async with asyncio.timeout(HTTP_TIMEOUT):
                _LOGGER.debug("Call to: %s", full_path)
                if method == "get":
                    response = await self.session.get(full_path, headers=headers)
                elif method == "post":
                    encoded_data = urlencode(data, encoding=self.api.get_encoding())
                    _LOGGER.debug("With payload: %s", data)
                    _LOGGER.debug("With payload (encoded): %s", encoded_data)
                    response = await self.session.post(
                        self.url + path, data=encoded_data, headers=headers
                    )
            if response is not None:
                _LOGGER.debug("Response path: %s", response.real_url.path)
                _LOGGER.debug("Response headers: %s", response.headers)
                _LOGGER.debug(
                    "Response body: %s", {await response.text(self.api.get_encoding())}
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
                    error_page_content = await response.text(self.api.get_encoding())
                    dom = pq(error_page_content)
                    error_element = dom(self.api.get_selector(Selector.ERROR_CODE))
                    if not error_element:
                        _LOGGER.error(error_page_content)
                        raise SomfyException("Unknown error")
                    error_code = error_element.text()
                    if (
                        error_code == SomfyError.NOT_AUTHORIZED
                        and not self.cookie
                        and retry is True
                    ):
                        await self.__login()
                        return await self.__do_call(
                            method, page, headers, data, retry=False, login=False
                        )
                    elif error_code == SomfyError.SESSION_ALREADY_OPEN:
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
                            raise SomfyException("Too many login retries")
                    elif error_code == SomfyError.WRONG_CREDENTIALS:
                        raise SomfyException("Login failed: Wrong credentials")
                    elif error_code == SomfyError.MAX_LOGIN_ATTEMPS:
                        raise SomfyException("Login failed: Max attempt count reached")
                    elif error_code == SomfyError.WRONG_CODE:
                        raise SomfyException("Login failed: Wrong code")
                    elif error_code == SomfyError.UNKNOWN_PARAMETER:
                        raise SomfyException("Command failed: Unknown parameter")
                    else:
                        _LOGGER.error(
                            "An unknonw error code was returned: %s", error_code
                        )
                        _LOGGER.error(
                            "Please report it with the page content below to the developer https://github.com/the8tre/somfy-protexial/issues"
                        )
                        _LOGGER.error(error_page_content)
                        raise SomfyException(
                            f"Command failed: Unknown errorCode: {error_code}"
                        )
                else:
                    return response
            else:
                raise SomfyException(f"Http error ({response.status})")
        except asyncio.TimeoutError as exception:
            raise RetryableSomfyException(
                f"Timeout error fetching information from {full_path}"
            ) from exception

        except ClientError as exception:
            raise SomfyException(
                f"ClientError fetching information from {full_path}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise SomfyException("Something really wrong happened!") from exception

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

    def load_api(self, api_type: ApiType):
        if api_type == ApiType.PROTEXIAL:
            return ProtexialApi()
        elif api_type == ApiType.PROTEXIAL_IO:
            return ProtexialIOApi()
        elif api_type == ApiType.PROTEXIOM:
            return ProtexiomApi()
        elif api_type is not None:
            raise SomfyException(f"Unknown api type: {type}")

    async def guess_and_set_api_type(self):
        for api_type in [ApiType.PROTEXIAL_IO, ApiType.PROTEXIAL, ApiType.PROTEXIOM]:
            self.api = self.load_api(api_type)
            has_version_page = False
            version_body = None
            # Some older systems don't have a version page
            version_page = self.api.get_page(Page.VERSION)
            if version_page is not None:
                has_version_page = True
                version_body = await self.do_guess_get(version_page)

            # Either the system doesn't have a version page, or the page was successfully retrieved
            if not has_version_page or version_body is not None:
                # Now check the login page
                login_page = self.api.get_page(Page.LOGIN)
                login_body = await self.do_guess_get(login_page)
                if login_body is not None:
                    # The system has a login page
                    dom = pq(login_body)
                    challenge_element = dom(
                        self.api.get_selector(Selector.LOGIN_CHALLENGE)
                    )
                    # Check if the challenge element is present
                    if challenge_element is not None:
                        challenge = challenge_element.text()
                        # Check that the challenge element looks fine
                        if re.match(CHALLENGE_REGEX, challenge):
                            self.api_type = api_type
                            return self.api_type
                        else:
                            _LOGGER.debug("Challenge not recognized: %s", challenge)
        raise SomfyException("Couldn't detect the centrale type")

    async def do_guess_get(self, page) -> str:
        try:
            async with asyncio.timeout(HTTP_TIMEOUT):
                _LOGGER.debug("Guess '%s'", self.url + page)
                response = await self.session.get(
                    self.url + page, headers={}, allow_redirects=False
                )
            if response.status == 200:
                response_body = await response.text(self.api.get_encoding())
                _LOGGER.debug("Guess response: %s", response_body)
                return response_body
            elif response.status == 302:
                raise SomfyException("Unavailable, please retry later")
            # Looks like another model
        except asyncio.TimeoutError as exception:
            raise SomfyException(
                f"Timeout error fetching from '{self.url + page}'"
            ) from exception
        except ClientError as exception:
            raise SomfyException(
                f"Error fetching from '{self.url + page}'"
            ) from exception
        except UnicodeDecodeError as exception:
            _LOGGER.error(
                "Incompatible encoding found in '%s' - %s", self.url + page, exception
            )
        except SomfyException:
            raise
        except Exception as exception:
            _LOGGER.error(
                "Something really wrong happened when fetching from '%s' ! - %s",
                self.url + page,
                exception,
            )
        return None

    async def get_challenge(self):
        login_response = await self.__do_call("get", Page.LOGIN, login=False)
        dom = pq(await login_response.text(self.api.get_encoding()))
        challenge_element = dom(self.api.get_selector(Selector.LOGIN_CHALLENGE))
        if challenge_element:
            return challenge_element.text()
        else:
            raise SomfyException("Challenge not found")

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

    async def get_status(self) -> Status:
        status = await self.do_get_status()
        if status.zoneA is None and status.zoneB is None and status.zoneC is None:
            # It seems the centrale doesn't return the status anylonger: Time to re-login
            await self.logout()
            status = await self.do_get_status(True)
        return status

    async def do_get_status(self, login_and_authenticated=False) -> Status:
        status_response = await self.__do_call(
            "get",
            Page.STATUS,
            login=login_and_authenticated,
            authenticated=login_and_authenticated
        )
        content = await status_response.text(self.api.get_encoding())
        status = self.extract_status(content)
        return status

    def extract_status(self, content) -> Status:
        response = ET.fromstring(content)
        status = Status()
        for child in response:
            filtered_child_text = self.filter_ascii(child.text)
            match child.tag:
                case "defaut0":
                    status.battery = filtered_child_text
                case "defaut1":
                    status.radio = filtered_child_text
                case "defaut2":
                    status.door = filtered_child_text
                case "defaut3":
                    status.alarm = filtered_child_text
                case "defaut4":
                    status.box = filtered_child_text
                case "zone0":
                    status.zoneA = filtered_child_text
                case "zone1":
                    status.zoneB = filtered_child_text
                case "zone2":
                    status.zoneC = filtered_child_text
                case "gsm":
                    status.gsm = filtered_child_text
                case "recgsm":
                    status.recgsm = filtered_child_text
                case "opegsm":
                    status.opegsm = filtered_child_text
                case "camera":
                    status.camera = filtered_child_text
        return status

    def filter_ascii(self, value) -> str:
        if value is None:
            return value
        filtered = "".join(filter(lambda x: x in _PRINTABLE_CHARS, value))
        return filtered.lower()

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
