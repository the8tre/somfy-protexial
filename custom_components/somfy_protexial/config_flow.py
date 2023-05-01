import logging
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import CONF_CODE, CONF_CODES, DOMAIN
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
            self.url = f'{parts.scheme}://{parts.netloc}'
            session = aiohttp_client.async_create_clientsession(self.hass)
            self.protexial = SomfyProtexial(session, self.url)
            try:
                challenge = await self.protexial.get_challenge()
                return await self.async_step_login(None, challenge)
            except Exception as e:
                _LOGGER.error(e)
                errors['base'] = 'connection'

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_URL, default="http://192.168.1.147"): cv.string}
            ),
            errors=errors
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
                
                return self.async_create_entry(title=self.url, data={
                    CONF_URL: self.url,
                    CONF_USERNAME: self.username,
                    CONF_PASSWORD: self.password,
                    CONF_CODES: self.codes,
                })
            except Exception as e:
                _LOGGER.error(e)
                errors['base'] = 'auth'

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
                    )
                }
            ),
            errors = errors
        )
