import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BINARY_SENSORS,
    COORDINATOR,
    DEVICE_INFO,
    DOMAIN,
    CONF_MONITORED_ELEMENTS,
    ELEMENT_DESCRIPTORS,
    ELEMENT_ENTITY,
)

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
        sensors.append(
            ProtexialAggregatedBinarySensor(device_info, coordinator, sensor)
        )

    monitored_elements = config_entry.data.get(CONF_MONITORED_ELEMENTS)
    elements_data = coordinator.data["elements"]

    for code in monitored_elements:
        element = next((x for x in elements_data if x["elt_code"] == code), None)
        if element is not None:
            descriptor = ELEMENT_DESCRIPTORS[element["item_type"]]
            device_name = f"{descriptor['name']}"
            device_name += (
                "" if len(element["elt_name"]) == 0 else f" - {element['elt_name']}"
            )
            device_info = DeviceInfo(
                identifiers={(DOMAIN, element["elt_code"])},
                name=device_name,
                manufacturer="Somfy",
            )
            for sensor_type in descriptor["sensors"]:
                sensor_info = ELEMENT_ENTITY[sensor_type]
                sensors.append(
                    ProtexialElementBinarySensor(
                        device_info, coordinator, code, sensor_info
                    )
                )

    async_add_entities(sensors)


class ProtexialAggregatedBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, device_info, coordinator, sensor: Any) -> None:
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
        return self.sensor["device_class"]

    def __getCurrentState(self):
        return (
            self.coordinator.data["aggregated"][self.sensor["id"]]
            == self.sensor["on_if"]
        )


class ProtexialElementBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, device_info, coordinator, code: str, sensor_info: Any) -> None:
        super().__init__(coordinator)
        self.code = code
        self._attr_unique_id = f"{DOMAIN}_{code}_{sensor_info['type']}"
        self._attr_device_info = device_info
        if "entity_category" in sensor_info:
            self._attr_entity_category = sensor_info["entity_category"]
        self.coordinator = coordinator
        self.sensor = sensor_info

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
        return self.sensor["device_class"]

    def __getCurrentState(self):
        element = next(
            (
                x
                for x in self.coordinator.data["elements"]
                if x["elt_code"] == self.code
            ),
            None,
        )
        return element[self.sensor["data_field"]] == self.sensor["on_if"]
