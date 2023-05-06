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

DEFAULT_COVER_NAME = "Volets"

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
    def __init__(self, device_info, api: SomfyProtexial):
        super().__init__()
        self._attr_unique_id = f"{DOMAIN}_control_cover"
        self._attr_device_info = device_info
        self.api = api

    @property
    def name(self):
        return DEFAULT_COVER_NAME

    @property
    def icon(self):
        return "mdi:roller-shade"

    @property
    def is_closed(self):
        # Can't determine cover state
        return None

    @property
    def device_class(self):
        return CoverDeviceClass.BLIND

    @property
    def supported_features(self):
        return (
            CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        )

    async def async_open_cover(self):
        await self.api.open_cover()

    async def async_close_cover(self):
        await self.api.close_cover()

    async def async_stop_cover(self):
        await self.api.stop_cover()
