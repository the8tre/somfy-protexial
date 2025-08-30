import logging
from dataclasses import dataclass

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityDescription,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.somfy_protexial.protexial_entity import (
    ProtexialBaseEntity,
    ProtexialEntityDescription,
)

from .const import API, COORDINATOR, DOMAIN
from .protexial import SomfyProtexial

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ProtexialCoverEntityDescription(
    ProtexialEntityDescription, CoverEntityDescription
):
    """Describes Cover entity."""


COVER_DESCRIPTION = ProtexialCoverEntityDescription(
    key="cover",
    translation_key="cover",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    lights = []
    lights.append(ProtexialCover(coordinator, config_entry, COVER_DESCRIPTION, api))
    async_add_entities(lights)


class ProtexialCover(ProtexialBaseEntity, CoverEntity):
    def __init__(
        self, coordinator, config_entry, description, api: SomfyProtexial
    ) -> None:
        super().__init__(coordinator, config_entry, description)
        self.api = api

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
