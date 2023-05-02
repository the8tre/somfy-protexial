import logging

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API
from .const import DOMAIN
from .protexial import SomfyProtexial

DEFAULT_LIGHT_NAME = "Somfy Protexial"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    lights = []
    lights.append(ProtexialLight(api))
    async_add_entities(lights)


class ProtexialLight(LightEntity):
    def __init__(self, api: SomfyProtexial):
        super().__init__()
        self.api = api
        self._changed_by = None
        self._state = False

    @property
    def name(self):
        return DEFAULT_LIGHT_NAME

    @property
    def icon(self):
        return "mdi:lightbulb-group"

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self):
        await self.api.turn_light_on()
        self._state = True

    async def async_turn_off(self):
        await self.api.turn_light_off()
        self._state = False
