import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import BINARY_SENSORS, COORDINATOR, DEVICE_INFO, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    sensors = []
    for sensor in BINARY_SENSORS:
        sensors.append(ProtexialBinarySensor(device_info, coordinator, sensor))
    async_add_entities(sensors)


class ProtexialBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, device_info, coordinator, sensor: Any):
        super().__init__(coordinator)
        self._attr_id = f"{DOMAIN}_sensor_{sensor['id']}"
        self._attr_unique_id = f"{DOMAIN}_sensor_{sensor['id']}"
        self._attr_device_info = device_info
        if "entity_category" in sensor:
            self._attr_entity_category = sensor["entity_category"]
        self.coordinator = coordinator
        self.sensor = sensor

    @property
    def name(self):
        """Return the name of the device."""
        return self.sensor["name"]

    @property
    def icon(self):
        return self.sensor["icon_on"] if self.is_on else self.sensor["icon_off"]

    @property
    def is_on(self) -> bool:
        return self.__getCurrentState()

    @property
    def state(self):
        if self.is_on:
            return self.sensor["state_on"]
        else:
            return self.sensor["state_off"]

    @property
    def device_class(self) -> BinarySensorDeviceClass:
        self.sensor["device_class"]

    def __getCurrentState(self):
        return self.coordinator.data[self.sensor["id"]] == self.sensor["on_if"]
