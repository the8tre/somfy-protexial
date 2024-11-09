import logging
import re
from typing import Any
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.const import (
    ATTR_SW_VERSION,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_URL,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
import voluptuous as vol

from .const import (
    ALL_ZONES,
    CONF_API_TYPE,
    CONF_ARM_CODE,
    CONF_CODE,
    CONF_CODES,
    CONF_HOME_ZONES,
    CONF_NIGHT_ZONES,
    DOMAIN,
    Zone,
)
from .protexial import SomfyProtexial

_LOGGER = logging.getLogger(__name__)


class ProtexialConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 3

    def __init__(self) -> None:
        super().__init__()
        self.url = None
        self.api_type = None
        self.protexial = None
        self.code = None
        self.username = None
        self.password = None

    async def async_step_user(self, user_input):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}
        if user_input is not None:
            parts = urlparse(user_input[CONF_URL].strip())
            self.url = f"{parts.scheme}://{parts.netloc}"
            session = aiohttp_client.async_create_clientsession(self.hass)
            self.protexial = SomfyProtexial(session, self.url)
            try:
                self.api_type = await self.protexial.guess_and_set_api_type()
                challenge = await self.protexial.get_challenge()
                return await self.async_step_login(None, challenge)
            except Exception as e:
                _LOGGER.exception(e)
                errors["base"] = "connection"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_URL): cv.string}),
            errors=errors,
        )

    async def async_step_login(self, user_input, challenge=None):
        errors = {}
        if user_input is not None:
            self.code = user_input[CONF_CODE]
            self.username = user_input[CONF_USERNAME]
            self.password = user_input[CONF_PASSWORD]

            try:
                self.codes = await self.protexial.get_challenge_card(
                    self.username, self.password, self.code
                )
                self.version = await self.protexial.get_version()

                return await self.async_step_config(None)
            except Exception as e:
                _LOGGER.error(e)
                errors["base"] = "auth"

        if challenge is None:
            challenge = await self.protexial.get_challenge()

        return self.async_show_form(
            step_id="login",
            description_placeholders={"challenge": challenge},
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default="u"): cv.string,
                    vol.Required(CONF_PASSWORD): cv.string,
                    vol.Required(CONF_CODE): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_config(self, user_input):
        errors = {}
        if user_input is not None:
            arm_code = (
                user_input[CONF_ARM_CODE] if CONF_ARM_CODE in user_input else None
            )

            if arm_code is not None and not re.match("^[0-9]{4}$", str(arm_code)):
                errors["base"] = "arm_code"
            elif (
                user_input[CONF_NIGHT_ZONES] != str(Zone.NONE.value)
                and user_input[CONF_NIGHT_ZONES] == user_input[CONF_HOME_ZONES]
            ):
                errors["base"] = "same_zones"
            else:
                night_zones = int(user_input[CONF_NIGHT_ZONES])
                home_zones = int(user_input[CONF_HOME_ZONES])
                return self.async_create_entry(
                    title=self.url,
                    data={
                        CONF_URL: self.url,
                        CONF_API_TYPE: self.api_type,
                        CONF_USERNAME: self.username,
                        CONF_PASSWORD: self.password,
                        CONF_CODES: self.codes,
                        CONF_NIGHT_ZONES: night_zones,
                        CONF_HOME_ZONES: home_zones,
                        CONF_ARM_CODE: arm_code,
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                        ATTR_SW_VERSION: self.version,
                    },
                )

        return self.async_show_form(
            step_id="config",
            errors=errors,
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NIGHT_ZONES,
                        default=str(Zone.NONE.value),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=ALL_ZONES,
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key="zones",
                        )
                    ),
                    vol.Required(
                        CONF_HOME_ZONES,
                        default=str(Zone.NONE.value),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=ALL_ZONES,
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key="zones",
                        )
                    ),
                    vol.Optional(CONF_ARM_CODE): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                    vol.Required(CONF_SCAN_INTERVAL, default=60): NumberSelector(
                        NumberSelectorConfig(
                            mode=NumberSelectorMode.BOX, min=15, max=3600, step=1
                        )
                    ),
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return ProtexialOptionsFlowHandler(config_entry)


class ProtexialOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Protexial options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors = {}
        if user_input is not None:
            arm_code = (
                user_input[CONF_ARM_CODE] if CONF_ARM_CODE in user_input else None
            )

            if arm_code is not None and not re.match("^[0-9]{4}$", str(arm_code)):
                errors["base"] = "arm_code"
            elif (
                user_input[CONF_NIGHT_ZONES] != str(Zone.NONE.value)
                and user_input[CONF_NIGHT_ZONES] == user_input[CONF_HOME_ZONES]
            ):
                errors["base"] = "same_zones"
            else:
                night_zones = int(user_input[CONF_NIGHT_ZONES])
                home_zones = int(user_input[CONF_HOME_ZONES])
                newData = {
                    CONF_URL: self.config_entry.data[CONF_URL],
                    CONF_API_TYPE: self.config_entry.data[CONF_API_TYPE],
                    CONF_USERNAME: self.config_entry.data[CONF_USERNAME],
                    CONF_PASSWORD: self.config_entry.data[CONF_PASSWORD],
                    CONF_CODES: self.config_entry.data[CONF_CODES],
                    CONF_NIGHT_ZONES: night_zones,
                    CONF_HOME_ZONES: home_zones,
                    CONF_ARM_CODE: arm_code,
                    CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    ATTR_SW_VERSION: self.config_entry.data[ATTR_SW_VERSION],
                }
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=newData, options=self.config_entry.options
                )
                return self.async_create_entry(title="", data={})

        current_night_zones = str(self.config_entry.data[CONF_NIGHT_ZONES])
        current_home_zones = str(self.config_entry.data[CONF_HOME_ZONES])

        return self.async_show_form(
            step_id="init",
            errors=errors,
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NIGHT_ZONES,
                        default=current_night_zones,
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=ALL_ZONES,
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key="zones",
                        )
                    ),
                    vol.Required(
                        CONF_HOME_ZONES,
                        default=current_home_zones,
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=ALL_ZONES,
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key="zones",
                        )
                    ),
                    vol.Optional(CONF_ARM_CODE): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.data[CONF_SCAN_INTERVAL],
                    ): NumberSelector(
                        NumberSelectorConfig(
                            mode=NumberSelectorMode.BOX, min=15, max=3600, step=1
                        )
                    ),
                }
            ),
        )
