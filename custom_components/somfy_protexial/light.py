import logging
from dataclasses import dataclass

from homeassistant.components.light import (
    ColorMode,
    LightEntity,
    LightEntityDescription,
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

DEFAULT_LIGHT_NAME = "Lumières"

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ProtexialCoverEntityDescription(
    ProtexialEntityDescription, LightEntityDescription
):
    """Describes Light entity."""


LIGHT_DESCRIPTION = ProtexialCoverEntityDescription(
    key="light",
    translation_key="light",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    lights = []
    lights.append(ProtexialLight(coordinator, config_entry, LIGHT_DESCRIPTION, api))
    async_add_entities(lights)


class ProtexialLight(ProtexialBaseEntity, LightEntity):
    def __init__(
        self, coordinator, config_entry, description, api: SomfyProtexial
    ) -> None:
        super().__init__(coordinator, config_entry, description)
        self.api = api
        self._changed_by = None
        self._state = False

    @property
    def is_on(self):
        return self._state

    @property
    def supported_color_modes(self):
        return {ColorMode.ONOFF}

    @property
    def color_mode(self):
        return ColorMode.ONOFF

    async def async_turn_on(self):
        await self.api.turn_light_on()
        self._state = True

    async def async_turn_off(self):
        await self.api.turn_light_off()
        self._state = False
