import logging
import re
from urllib.parse import urlparse

from homeassistant import config_entries
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntityFeature
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_URL,
    CONF_USERNAME,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
)
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
import voluptuous as vol

from .const import CONF_ARM_CODE, CONF_CODE, CONF_CODES, CONF_MODES, DOMAIN
from .protexial import SomfyProtexial

_LOGGER = logging.getLogger(__name__)


class ProtexialConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}
        if user_input is not None:
            parts = urlparse(user_input[CONF_URL])
            self.url = f"{parts.scheme}://{parts.netloc}"
            session = aiohttp_client.async_create_clientsession(self.hass)
            self.protexial = SomfyProtexial(session, self.url)
            try:
                challenge = await self.protexial.get_challenge()
                return await self.async_step_login(None, challenge)
            except Exception as e:
                _LOGGER.error(e)
                errors["base"] = "connection"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_URL): cv.string}
            ),
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
            arm_code = user_input[CONF_ARM_CODE] if CONF_ARM_CODE in user_input else None
            if arm_code is None or re.match("^[0-9]{4}$", str(arm_code)):
                modes = []
                # if user_input[STATE_ALARM_ARMED_AWAY]:
                modes.append(AlarmControlPanelEntityFeature.ARM_AWAY)
                if user_input[STATE_ALARM_ARMED_NIGHT]:
                    modes.append(AlarmControlPanelEntityFeature.ARM_NIGHT)
                if user_input[STATE_ALARM_ARMED_HOME]:
                    modes.append(AlarmControlPanelEntityFeature.ARM_HOME)
                return self.async_create_entry(
                    title=self.url,
                    data={
                        CONF_URL: self.url,
                        CONF_USERNAME: self.username,
                        CONF_PASSWORD: self.password,
                        CONF_CODES: self.codes,
                        CONF_MODES: modes,
                        CONF_ARM_CODE: arm_code,
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    },
                )
            else:
                errors["base"] = "arm_code"

        return self.async_show_form(
            step_id="config",
            errors=errors,
            data_schema=vol.Schema(
                {
                    # vol.Required(STATE_ALARM_ARMED_AWAY, default=True): cv.boolean,
                    vol.Optional(STATE_ALARM_ARMED_NIGHT, default=False): cv.boolean,
                    vol.Optional(STATE_ALARM_ARMED_HOME, default=False): cv.boolean,
                    vol.Optional(CONF_ARM_CODE): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                    vol.Required(CONF_SCAN_INTERVAL, default=20): NumberSelector(
                        NumberSelectorConfig(
                            mode=NumberSelectorMode.BOX, min=15, max=3600, step=1
                        )
                    ),
                }
            ),
        )
