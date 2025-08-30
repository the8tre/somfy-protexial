from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_SW_VERSION,
    CONF_URL,
)
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


@dataclass(frozen=True, kw_only=True)
class ProtexialEntityDescription(EntityDescription):
    """Describes Example sensor entity."""

    has_entity_name = True


class ProtexialBaseEntity(CoordinatorEntity):
    config_entry: ConfigEntry
    entity_description: ProtexialEntityDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_description: ProtexialEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_description = entity_description
        self._attr_unique_id = f"{entity_description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, "centrale")},
            connections={(CONNECTION_NETWORK_MAC, self.config_entry.data[CONF_URL])},
            name="Somfy Protexial",
            manufacturer="Somfy",
            model="Protexial",
            sw_version=self.config_entry.data[ATTR_SW_VERSION],
        )
