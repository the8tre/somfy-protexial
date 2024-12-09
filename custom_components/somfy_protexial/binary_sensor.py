import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import COORDINATOR, DEVICE_INFO, DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ProtexialSensorEntityDescription(BinarySensorEntityDescription):
    """Describes Example sensor entity."""

    value_fn: Callable[[str], bool]


BINARY_SENSORS: tuple[ProtexialSensorEntityDescription, ...] = (
    ProtexialSensorEntityDescription(
        key="global_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="global_battery",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorEntityDescription(
        key="global_alarm",
        device_class=BinarySensorDeviceClass.MOTION,
        translation_key="global_alarm",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorEntityDescription(
        key="global_opening",
        device_class=BinarySensorDeviceClass.DOOR,
        translation_key="global_opening",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorEntityDescription(
        key="global_box",
        device_class=BinarySensorDeviceClass.PROBLEM,
        translation_key="global_box",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorEntityDescription(
        key="global_radio",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="global_radio",
        value_fn=lambda value: value == "ok",
    ),
    ProtexialSensorEntityDescription(
        key="gsm",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="gsm",
        value_fn=lambda value: value
        == "gsm connect au rseau",  # Filtered: "GSM connecté au réseau"
    ),
    ProtexialSensorEntityDescription(
        key="camera",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="camera",
        value_fn=lambda value: value == "enabled",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    async_add_entities(
        ProtexialBinarySensor(device_info, coordinator, description)
        for description in BINARY_SENSORS
    )


class ProtexialBinarySensor(CoordinatorEntity, BinarySensorEntity):
    entity_description: ProtexialSensorEntityDescription

    def __init__(
        self,
        device_info: DeviceInfo,
        coordinator: DataUpdateCoordinator,
        entity_description: ProtexialSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.device_info = device_info
        self.entity_description = entity_description
        self._attr_unique_id = f"{entity_description.key}"

    @property
    def is_on(self) -> bool:
        return self.__get_current_state()

    def __get_current_state(self) -> bool:
        value = self.coordinator.data[self.entity_description.key]
        return self.entity_description.value_fn(value)
