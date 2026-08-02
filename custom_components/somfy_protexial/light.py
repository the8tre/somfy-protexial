import logging

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API, DEVICE_INFO, DOMAIN
from .protexial import SomfyProtexial

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
    _attr_has_entity_name = True
    _attr_translation_key = "light"
    _attr_icon = "mdi:lightbulb-group"
    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF

    def __init__(self, device_info, api: SomfyProtexial) -> None:
        super().__init__()
        self.api = api
        self._attr_unique_id = f"{DOMAIN}_control_light"
        self._attr_device_info = device_info
        self._changed_by = None
        self._state = False


    @property
    def is_on(self):
        return self._state


    async def async_turn_on(self):
        await self.api.turn_light_on()
        self._state = True

    async def async_turn_off(self):
        await self.api.turn_light_off()
        self._state = False
