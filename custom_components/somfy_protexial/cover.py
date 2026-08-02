import logging

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
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
    lights.append(ProtexialCover(device_info, api))
    async_add_entities(lights)


class ProtexialCover(CoverEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "cover"
    _attr_icon = "mdi:roller-shade"
    _attr_device_class = CoverDeviceClass.BLIND
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
    )

    def __init__(self, device_info, api: SomfyProtexial) -> None:
        super().__init__()
        self._attr_unique_id = f"{DOMAIN}_control_cover"
        self._attr_device_info = device_info
        self.api = api


    @property
    def is_closed(self):
        # Can't determine cover state
        return None


    async def async_open_cover(self):
        await self.api.open_cover()

    async def async_close_cover(self):
        await self.api.close_cover()

    async def async_stop_cover(self):
        await self.api.stop_cover()
