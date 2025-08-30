import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_SW_VERSION,
    CONF_URL,
    EntityCategory,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from custom_components.somfy_protexial.protexial_entity import (
    ProtexialBaseEntity,
    ProtexialEntityDescription,
)

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ProtexialSensorBinaryEntityDescription(
    ProtexialEntityDescription, BinarySensorEntityDescription
):
    """Describes Binary sensor entity."""

    value_fn: Callable[[str], bool]


BINARY_SENSORS: tuple[ProtexialSensorBinaryEntityDescription, ...] = (
    ProtexialSensorBinaryEntityDescription(
        key="global_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="global_battery",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorBinaryEntityDescription(
        key="global_alarm",
        device_class=BinarySensorDeviceClass.MOTION,
        translation_key="global_alarm",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorBinaryEntityDescription(
        key="global_opening",
        device_class=BinarySensorDeviceClass.DOOR,
        translation_key="global_opening",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorBinaryEntityDescription(
        key="global_box",
        device_class=BinarySensorDeviceClass.PROBLEM,
        translation_key="global_box",
        value_fn=lambda value: value != "ok",
    ),
    ProtexialSensorBinaryEntityDescription(
        key="global_radio",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="global_radio",
        value_fn=lambda value: value == "ok",
    ),
    ProtexialSensorBinaryEntityDescription(
        key="gsm",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        translation_key="gsm",
        value_fn=lambda value: value
        == "gsm connect au rseau",  # Filtered: "GSM connecté au réseau"
    ),
    ProtexialSensorBinaryEntityDescription(
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
    async_add_entities(
        ProtexialBinarySensor(coordinator, config_entry, description)
        for description in BINARY_SENSORS
    )


class ProtexialBinarySensor(ProtexialBaseEntity, BinarySensorEntity):
    @property
    def is_on(self) -> bool:
        return self.__get_current_state()

    def __get_current_state(self) -> bool:
        value = self.coordinator.data[self.entity_description.key]
        return cast(
            ProtexialSensorBinaryEntityDescription, self.entity_description
        ).value_fn(value)
