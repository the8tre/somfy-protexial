import logging
from typing import Any, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory

from .const import BINARY_SENSORS, COORDINATOR, DEVICE_INFO, DOMAIN

_LOGGER = logging.getLogger(__name__)

# Sensor type -> flags mapping (used to decide which flags to expose)
ELEMENTS_MAPPING = {
    "badge": ["house", "pause"],
    "dm": ["battery", "comm", "house", "tamper", "pause"],
    "dm image": ["battery", "comm", "house", "tamper", "pause"],
    "cl lcd": ["battery", "comm", "house", "tamper", "pause"],
    "clavier": ["battery", "comm", "house", "tamper", "pause"],
    "do": ["battery", "comm", "house", "tamper", "door", "pause"],
    "do vitre": ["battery", "comm", "house", "tamper", "door", "pause"],
    "do gar": ["battery", "comm", "house", "tamper", "door", "pause"],
    "d. fumée": ["battery", "comm", "house", "pause"],
    # robust alias for mojibake/variants
    "d. fum": ["battery", "comm", "house", "pause"],
    "tc multi": ["house", "pause"],
    "tc 4": ["house", "pause"],
    "sir int": ["battery", "comm", "house", "tamper", "pause"],
    "sir ext": ["battery", "comm", "house", "tamper", "pause"],
    "tr tél": ["battery", "comm", "house", "tamper", "pause"],
    # robust aliases for mojibake/variants
    "tr t": ["battery", "comm", "house", "tamper", "pause"],
}

# Field configuration (class/icon). Note: we interpret flags per-field in code.
FIELD_CONFIG = {
    "battery": {"class": BinarySensorDeviceClass.BATTERY, "icon": "mdi:battery"},
    "comm": {"class": BinarySensorDeviceClass.CONNECTIVITY, "icon": "mdi:radio-tower"},
    "house": {"class": BinarySensorDeviceClass.PROBLEM, "icon": "mdi:home-alert"},
    "tamper": {"class": BinarySensorDeviceClass.TAMPER, "icon": "mdi:shield-alert"},
    "door": {"class": BinarySensorDeviceClass.DOOR, "icon": "mdi:door-closed"},
    "pause": {"class": BinarySensorDeviceClass.RUNNING, "icon": "mdi:pause-circle"},
}


# Default icon for an element
def _get_element_icon(element: dict, problem: bool = False) -> str:
    """Return the appropriate icon for a Somfy element."""

    label = (element.get("label") or "").lower()
    name = (element.get("name") or "").lower()

    element_type = f"{label} {name}"

    if "vitre" in element_type:
        return "mdi:window-open-variant" if problem else "mdi:window-closed-variant"

    if "ouvt" in element_type:
        return "mdi:door-open" if problem else "mdi:door-closed"

    if "do gar" in element_type:
        return "mdi:garage-open-variant" if problem else "mdi:garage-variant"

    if "dm" in element_type:
        return "mdi:motion-sensor-off" if problem else "mdi:motion-sensor"

    if "fum" in element_type:
        return (
            "mdi:smoke-detector-variant-alert"
            if problem
            else "mdi:smoke-detector-variant"
        )

    if "sir ext" in element_type:
        return "mdi:home-sound-out-outline" if problem else "mdi:home-sound-out"

    if "sir" in element_type:
        return "mdi:bullhorn-outline" if problem else "mdi:bullhorn"

    if "clavier" in element_type or "cl lcd" in element_type:
        return "mdi:keyboard-off-outline" if problem else "mdi:dialpad"

    if "tc" in element_type:
        return "mdi:remote-off" if problem else "mdi:remote"

    if "badge" in element_type:
        return "mdi:key-alert" if problem else "mdi:key-variant"

    if "tr" in element_type:
        return "mdi:alpha-s-box-outline" if problem else "mdi:alpha-s-box"

    return "mdi:alert-rhombus-outline" if problem else "mdi:help-rhombus"


def _fields_for_label(label: str) -> Optional[list[str]]:
    """Return the list of flags to expose for a given element label (prefix match)."""
    lab = (label or "").strip().lower()
    for key in sorted(ELEMENTS_MAPPING.keys(), key=len, reverse=True):
        if lab.startswith(key):
            return ELEMENTS_MAPPING[key]
    return None


def log_element(el: dict, logger):
    """Dump the full element dict to logs for debugging."""
    logger.debug("==== DUMP ELEMENT ====")
    for k, v in el.items():
        logger.debug("  %s: %s", k, v)
    logger.debug("======================")


def get_raw_flag(field: str, el: dict) -> str:
    """Return the raw value for a given flag, tolerating multiple key names."""
    key_map = {
        "battery": ["battery", "elt_pile", "pile"],
        "comm": ["comm", "elt_onde", "onde"],
        "house": ["house", "elt_maison", "maison"],
        "tamper": ["tamper", "elt_as", "as"],
        "door": ["door", "elt_porte", "porte"],
        "pause": ["pause", "item_pause"],
    }
    keys = key_map.get(field)
    if not keys:
        # Unknown flag → avoid crashing
        _LOGGER.debug(
            "get_raw_flag: unknown field '%s' for element %s", field, el.get("name")
        )
        return ""

    for k in keys:
        v = el.get(k)
        if v is None:
            continue
        vs = str(v).strip().lower()
        if vs:
            return vs
    return ""


@property
def is_on(self) -> bool:
    """Aggregate boolean: True if at least one relevant flag is in a 'problem' state."""
    el = self._find_element() or self._element
    if not el:
        return False

    # A problem is detected if any attribute is NOK
    fields = getattr(self, "_fields", [])
    for field in fields:
        val = self._normalize_flag(field, el.get(field))
        if val is False:  # False = problem detected
            return True
    return False


def _normalize_zone_code(z: str) -> str | None:
    """Normalize zone codes like 'A (f)'/'AT (f)' to 'A', keep 'SYS'/'TEC', else None."""
    if not z:
        return None
    zl = z.strip().upper()
    if zl.startswith("AT"):
        return "A"
    if zl.startswith("A"):
        return "A"
    if zl.startswith("B"):
        return "B"
    if zl.startswith("C"):
        return "C"
    if zl.startswith("SYS"):
        return "SYS"
    if zl.startswith("TEC"):
        return "TEC"
    return None


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors (static from status.xml and dynamic from elements page)."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    sensors = []

    # Static binary sensors from status.xml
    for sensor in BINARY_SENSORS:
        description = BinarySensorEntityDescription(
            key=sensor["id"],
            translation_key=sensor["translation_key"],
            device_class=sensor.get("device_class"),
            entity_category=sensor.get("entity_category"),
        )
        sensors.append(
            ProtexialBinarySensor(device_info, coordinator, description, sensor)
        )

    # Dynamic binary sensors (u_plistelmt.htm): one aggregate per element
    elements = (coordinator.data or {}).get("elements", [])
    for el in elements:
        # 1) Aggregated sensor (single binary per element)
        sensors.append(SomfyElementAggregateBinarySensor(coordinator, el, device_info))

        # 2) Detailed sensors (disabled by design, keep commented)
        fields = _fields_for_label(el.get("label"))
        if not fields:
            continue

        # for field in fields:
        #     cfg = FIELD_CONFIG[field].copy()
        #     # If label contains "vitre" and this is a door flag, prefer WINDOW class
        #     if field == "door" and "vitre" in (el.get("label", "").lower()):
        #         cfg["class"] = BinarySensorDeviceClass.WINDOW
        #     sensors.append(
        #         SomfyElementBinarySensor(
        #             coordinator, el, field, cfg, device_info
        #         )
        #     )

    async_add_entities(sensors)


class ProtexialBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor backed by status.xml."""

    _attr_has_entity_name = True

    def __init__(
        self,
        device_info,
        coordinator,
        description: BinarySensorEntityDescription,
        sensor: dict[str, Any],
    ) -> None:
        """Initialize a translated static binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_translation_key = description.translation_key
        self._attr_unique_id = f"{DOMAIN}_sensor_{description.key}"
        self._attr_device_info = device_info
        self.sensor = sensor

    @property
    def icon(self) -> str | None:
        """Return a dynamic icon based on state."""
        return self.sensor.get("icon_on") if self.is_on else self.sensor.get("icon_off")

    @property
    def is_on(self) -> bool:
        """Return True if the underlying status value represents 'on'."""
        value = (self.coordinator.data or {}).get(self.entity_description.key)
        if "on_if" in self.sensor:
            return value == self.sensor["on_if"]
        return value != self.sensor["off_if"]


class SomfyElementBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """One binary sensor per flag (battery/comm/house/tamper/door) for each element."""

    def __init__(self, coordinator, element, field: str, cfg: dict, device_info):
        """Build a detailed per-flag sensor tied to one element."""
        super().__init__(coordinator)
        self._code = element.get("code") or ""
        self._label = (element.get("label") or "").strip()
        self._name_part = (element.get("name") or "").strip()
        self._field = field
        self._cfg = cfg

        self._attr_unique_id = f"{DOMAIN}_elt_{self._code}_{self._field}"
        self._attr_device_info = device_info
        human_field = {
            "battery": "batterie",
            "comm": "radio",
            "house": "défaut",
            "tamper": "arrachement",
            "door": "ouverture",
        }.get(self._field, self._field)
        self._attr_name = f"{self._label} - {self._name_part} ({human_field})".strip(
            " -"
        )
        self._attr_device_class = cfg.get("class")
        self._icon = cfg.get("icon")

    @property
    def icon(self):
        """Return the icon configured for this flag."""
        return self._icon

    def _find_element(self) -> dict | None:
        """Find the current element payload by code from coordinator data."""
        elements = (self.coordinator.data or {}).get("elements", [])
        for e in elements:
            if e.get("code") == self._code:
                return e
        return None

    @property
    def is_on(self) -> bool:
        """Interpret this flag for the element: True means 'problem', unless noted."""
        el = self._find_element()
        if not el:
            return False

        raw = get_raw_flag(self._field, el)

        # Field-specific interpretation
        if self._field == "battery":
            # True when battery is low (itembattok = OK)
            return raw != "itembattok"

        if self._field == "comm":
            # True when radio link is OK
            return raw in ("itemcomok", "itemboxok")

        if self._field == "house":
            # True when a domestic fault/intrusion is present (itemhouseok = OK)
            return raw != "itemhouseok"

        if self._field == "tamper":
            # True when tamper is triggered (itemboxok = OK)
            return raw != "itemboxok"

        if self._field == "door":
            # True when door/window is open (itemdoorok = closed)
            return raw != "itemdoorok"

        if self._field == "pause":
            # You chose: running = True, paused = False
            return raw == "running"

        return False

    def _handle_coordinator_update(self) -> None:
        """Push state on coordinator refresh."""
        self.async_write_ha_state()


class SomfyElementAggregateBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """
    Single binary sensor per element, aggregating all its flags.
    ON = a problem is detected (low battery, lost link, tamper, door open, domestic fault, etc.).
    """

    def __init__(self, coordinator, element, device_info):
        """Build the aggregate sensor for one element (diagnostic category)."""
        super().__init__(coordinator)
        self._code = element.get("code") or ""
        self._label = (element.get("label") or "").strip()
        self._name_part = (element.get("name") or "").strip()
        self._element = element  # initial snapshot
        self._attr_unique_id = f"{DOMAIN}_elt_{self._code}_aggregate"
        self._attr_device_info = device_info
        self._attr_name = f"{self._label} - {self._name_part}"
        self._attr_translation_key = "element_aggregate"
        self._attr_device_class = BinarySensorDeviceClass.PROBLEM
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        # self._attr_icon = _get_element_icon(element)
        # self._icon = _get_element_icon(element)
        self._icon_on = _get_element_icon(element, problem=True)
        self._icon_off = _get_element_icon(element, problem=False)

        self._fields = _fields_for_label(self._label) or []
        if "pause" in element and "pause" not in self._fields:
            self._fields.append("pause")

    @property
    def icon(self) -> str | None:
        """Return the icon according to the aggregate state."""
        if self.is_on:
            return self._icon_on
        return self._icon_off

    def _normalize_flag(self, field: str, raw: str | None) -> bool | None:
        """Convert a raw flag into boolean (True=OK, False=not OK)."""
        if not raw:
            return None
        raw = str(raw).lower()

        if field == "battery":
            return raw == "itembattok"
        if field == "comm":
            return raw in ("itemcomok", "itemboxok")
        if field == "house":
            return raw == "itemhouseok"
        if field == "tamper":
            return raw == "itemboxok"
        if field == "door":
            return raw == "itemdoorok"
        if field == "pause":
            return raw == "running"
        return None

    def _value_for(self, field: str, el: dict) -> tuple[bool | None, str | None]:
        """Return (ok_bool, human_value) for a given field."""
        raw = (el or {}).get(field)
        ok = self._normalize_flag(field, raw)

        if ok is None:
            return None, None

        if field == "battery":
            human = "ok" if ok else "low"
        elif field == "comm":
            human = "connected" if ok else "disconnected"
        elif field == "house":
            human = "ok" if ok else "domestic fault/intrusion"
        elif field == "tamper":
            human = "ok" if ok else "open/ripped off"
        elif field == "door":
            human = "closed" if ok else "open"
        elif field == "pause":
            human = "running" if ok else "paused"
        else:
            human = None

        return ok, human

    def _find_element(self) -> dict | None:
        """Find the current element payload by code from coordinator data."""
        elements = (self.coordinator.data or {}).get("elements", [])
        for e in elements:
            if e.get("code") == self._code:
                return e
        return None

    def _raw(self, el: dict, field: str) -> str:
        """Return the raw flag value for a field (with aliases)."""
        aliases = {
            "elt_pile": ["battery", "elt_pile", "pile"],
            "elt_onde": ["comm", "elt_onde", "onde"],
            "elt_maison": ["house", "elt_maison", "maison"],
            "elt_as": ["tamper", "elt_as", "as"],
            "elt_porte": ["door", "elt_porte", "porte"],
            "pause": ["pause"],
        }.get(field, [field])

        for k in aliases:
            v = el.get(k)
            if v is not None and v != "":
                return str(v).strip().lower()
        return ""

    def _is_problem_for_field(self, field: str, raw: str) -> bool:
        """Problem rule for each flag (True = problem)."""
        if field == "elt_pile":
            # itembattok = OK -> problem if different
            return raw != "itembattok"
        if field == "elt_onde":
            # link OK if itemcomok or itemboxok -> else problem
            return raw not in ("itemcomok", "itemboxok")
        if field == "elt_maison":
            # itemhouseok = OK -> problem if different
            return raw != "itemhouseok"
        if field == "elt_as":
            # itemboxok = OK -> problem if different (tamper)
            return raw != "itemboxok"
        if field == "elt_porte":
            # itemdoorok = closed -> problem if different (open)
            return raw != "itemdoorok"
        if field == "pause":
            # running = OK -> paused means problem
            return raw == "paused"
        return False

    @property
    def is_on(self) -> bool:
        """True when any relevant field indicates a problem; False when all OK."""
        el = self._find_element() or self._element or {}
        fields = getattr(self, "_fields", [])
        for field in fields:
            ok, _ = self._value_for(field, el)
            if ok is False:
                return True
        return False

    @property
    def extra_state_attributes(self) -> dict:
        """Expose only the requested human-friendly attributes plus Zone."""
        el = self._find_element() or self._element or {}
        fields = getattr(self, "_fields", [])

        # (internal_name, exposed_label)
        order = [
            ("battery", "Battery"),
            ("comm", "Link"),
            ("house", "House"),
            ("tamper", "Tamper"),
            ("door", "Door open"),
            ("pause", "Running"),
        ]

        attrs: dict[str, str] = {}
        for field, label in order:
            if field not in fields:
                continue
            _, human = self._value_for(field, el)
            if human is not None:
                attrs[label] = human

        # Add zone once if available
        zone = el.get("zone")
        if zone:
            attrs["Zone"] = zone

        return attrs

    def _handle_coordinator_update(self) -> None:
        """Push state and attributes on coordinator refresh."""
        self.async_write_ha_state()
