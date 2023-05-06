import logging

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API, DEVICE_INFO, DOMAIN
from .protexial import SomfyProtexial

DEFAULT_LIGHT_NAME = "Lumières"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    lights = []
    lights.append(ProtexialLight(device_info, api))
    async_add_entities(lights)


class ProtexialLight(LightEntity):
    def __init__(self, device_info, api: SomfyProtexial):
        super().__init__()
        self.api = api
        self._attr_unique_id = f"{DOMAIN}_control_light"
        self._attr_device_info = device_info
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
