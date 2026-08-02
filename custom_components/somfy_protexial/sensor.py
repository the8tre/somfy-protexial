# Sensors (GSM + zones from elements)
import logging
from typing import Any, Iterable

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import SENSORS, COORDINATOR, DEVICE_INFO, DOMAIN

_LOGGER = logging.getLogger(__name__)


# ---------- Utils ----------
def _collect_zone_options(elements: Iterable[dict]) -> list[str]:
    """Build an enum options list from actually observed zones."""
    zones = {e.get("zone", "") for e in (elements or []) if e.get("zone")}
    # keep stable order: SYS first, then alpha
    ordered = ["SYS"] + sorted(z for z in zones if z != "SYS")
    return ordered or ["SYS"]


def _find_element_by_code(elements: list[dict], code: str) -> dict | None:
    """Find an element dict by its 'code' field."""
    for e in elements or []:
        if e.get("code") == code:
            return e
    return None


# ---------- Setup ----------
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform (GSM sensors + optional per-element zone sensor)."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]

    entities: list[SensorEntity] = []

    # 1) Predefined sensors in SENSORS (GSM provider, signal, etc.)
    for sensor in SENSORS:
        description = SensorEntityDescription(
            key=sensor["id"],
            translation_key=sensor["translation_key"],
            device_class=sensor.get("device_class"),
            icon=sensor.get("icon"),
            entity_category=sensor.get("entity_category"),
            suggested_display_precision=sensor.get("suggested_display_precision"),
        )
        entities.append(ProtexialSensor(device_info, coordinator, description))

    # 2) Per-element zone sensors (ENUM) from u_plistelmt.htm (kept commented by design)
    elements = (coordinator.data or {}).get("elements", [])
    zone_options = _collect_zone_options(elements)

    # for el in elements:
    #     # Create a unique 'zone' sensor per element
    #     code = el.get("code")
    #     name = el.get("name")
    #     label = el.get("label")
    #     if not code:
    #         continue
    #     entities.append(
    #         SomfyElementZoneSensor(
    #             element_code=code,
    #             element_label=label or "",
    #             element_name=name or "",
    #             device_info=device_info,
    #             coordinator=coordinator,
    #             options=zone_options,
    #         )
    #     )

    if entities:
        async_add_entities(entities)
    else:
        _LOGGER.debug("No sensors to add (SENSORS + zones).")


# ---------- Existing sensors (GSM, etc.) ----------
class ProtexialSensor(CoordinatorEntity, SensorEntity):
    """Representation of a translated Protexial sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        device_info,
        coordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the entity from its native description."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_translation_key = description.translation_key
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_device_info = device_info
        self._native_value = None

    @property
    def native_value(self):
        """Return the native value exposed to Home Assistant."""
        return self._native_value

    def _handle_coordinator_update(self) -> None:
        """Handle updated coordinator data."""
        value = (self.coordinator.data or {}).get(self.entity_description.key)

        if self.entity_description.key == "recgsm" and value is not None:
            try:
                normalized = str(value).strip().lower()
                if normalized.startswith("k"):
                    normalized = normalized[1:]
                self._native_value = int(normalized)
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Unexpected GSM signal value '%s' for sensor '%s'",
                    value,
                    self.entity_description.key,
                )
                self._native_value = None
        elif self.entity_description.key == "opegsm" and value is not None:
            self._native_value = str(value).replace('"', "").strip()
        else:
            self._native_value = value

        self.async_write_ha_state()


# ---------- Per-element zone sensors (commented) ----------
# class SomfyElementZoneSensor(CoordinatorEntity, SensorEntity):
#     """ENUM zone sensor based on u_plistelmt.htm for a given element."""
#
#     _attr_device_class = SensorDeviceClass.ENUM
#
#     def __init__(
#         self,
#         element_code: str,
#         element_label: str,
#         element_name: str,
#         device_info,
#         coordinator,
#         options: list[str],
#     ):
#         """Build the per-element zone sensor."""
#         super().__init__(coordinator)
#         self._code = element_code
#         self._label = element_label
#         self._name_part = element_name
#         self._attr_name = f"{element_label} - {element_name} (zone)".strip(" -")
#         self._attr_unique_id = f"{DOMAIN}_element_zone_{element_code}"
#         self._attr_device_info = device_info
#         self._attr_options = options
#         self._native_value = None  # updated on refresh
#
#     @property
#     def native_value(self):
#         """Return the current zone value."""
#         return self._native_value
#
#     def _handle_coordinator_update(self) -> None:
#         """Pick up the current zone from coordinator.data['elements']."""
#         payload = self.coordinator.data or {}
#         elements = payload.get("elements", [])
#         el = _find_element_by_code(elements, self._code)
#         new_zone = el.get("zone") if el else None
#
#         # If a new value shows up, add it to options
#         if new_zone and isinstance(self._attr_options, list) and new_zone not in self._attr_options:
#             self._attr_options = self._attr_options + [new_zone]
#
#         self._native_value = new_zone
#         self.async_write_ha_state()
