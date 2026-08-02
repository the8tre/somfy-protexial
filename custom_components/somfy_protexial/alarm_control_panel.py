from functools import reduce
import logging

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
    CodeFormat,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    API,
    CONF_ARM_CODE,
    CONF_HOME_ZONES,
    CONF_NIGHT_ZONES,
    COORDINATOR,
    DEVICE_INFO,
    DOMAIN,
    Zone,
)
from .helper import int_to_zones

ACTIVATION_ALARM_CODE = None
ALARM_STATE = None

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create and register the alarm control panel entity."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    night_zones = config_entry.data.get(CONF_NIGHT_ZONES)
    home_zones = config_entry.data.get(CONF_HOME_ZONES)
    arm_code = config_entry.data.get(CONF_ARM_CODE)
    alarms = []
    alarms.append(
        ProtexialAlarm(device_info, coordinator, api,
                       night_zones, home_zones, arm_code)
    )
    async_add_entities(alarms)


class ProtexialAlarm(CoordinatorEntity, AlarmControlPanelEntity):
    """Alarm control panel that mirrors the centrale's arming state."""

    _attr_has_entity_name = True
    _attr_translation_key = "alarm"
    _attr_icon = "mdi:shield-home"

    def __init__(
        self, device_info, coordinator, api, night_zones, home_zones, arm_code
    ) -> None:
        """Initialize entity metadata and supported modes."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_control_alarm"
        self._attr_device_info = device_info
        self.coordinator = coordinator
        self.api = api
        self.night_zones = night_zones
        self.home_zones = home_zones
        self.modes = [AlarmControlPanelEntityFeature.ARM_AWAY]
        if self.night_zones > 0:
            self.modes.append(AlarmControlPanelEntityFeature.ARM_NIGHT)
        if self.home_zones > 0:
            self.modes.append(AlarmControlPanelEntityFeature.ARM_HOME)
        self.arm_code = arm_code
        self._changed_by = None


    @property
    def supported_features(self) -> int:
        """Return the bitmask of supported features."""
        return reduce(lambda a, b: a | b, self.modes)

    @property
    def code_format(self):
        """Return the required code format for arming/disarming."""
        if self.arm_code is None:
            return None
        else:
            return CodeFormat.NUMBER

    @property
    def code_arm_required(self) -> bool:
        """Whether a code is required to arm/disarm."""
        return self.arm_code is not None

    @property
    def changed_by(self):
        """Who triggered the last change (unused for now)."""
        return self._changed_by

    @property
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the current alarm state."""
        return self.__getCurrentState()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Propagate coordinator refresh to HA state."""
        self.async_write_ha_state()

    def __getCurrentState(self):
        """Determine the current state using a dict (fallback to attributes if needed)."""
        data = self.coordinator.data or {}

        def val(key: str):
            if isinstance(data, dict):
                return data.get(key)
            # Fallback if data is an object with attributes
            return getattr(data, key, None)

        active_zones = Zone.NONE.value
        if val("zoneA") == "on":
            active_zones += Zone.A.value
        if val("zoneB") == "on":
            active_zones += Zone.B.value
        if val("zoneC") == "on":
            active_zones += Zone.C.value

        if active_zones == Zone.NONE.value:
            return AlarmControlPanelState.DISARMED

        # status.xml's "alarm" field (defaut3) is the centrale's own
        # "Alarme déclenchée" flag (Jeedom's phpProtexiom client names it
        # ALARM/"Alarm trggered OK/nok_int" and maps a dedicated "alarm"
        # info cmd to it). While armed, if this flag is not "ok", the siren
        # is actually sounding - report the dedicated TRIGGERED state
        # rather than just the armed mode, so dashboards/automations can
        # react to an active intrusion specifically. (While disarmed this
        # flag can also reflect mere motion detection - already exposed
        # separately as the "Mouvement" binary_sensor - so it's only
        # treated as a real trigger here once a zone is actually armed.)
        if val("alarm") not in (None, "ok"):
            return AlarmControlPanelState.TRIGGERED

        if active_zones == Zone.ABC.value:
            return AlarmControlPanelState.ARMED_AWAY

        if active_zones == self.night_zones:
            return AlarmControlPanelState.ARMED_NIGHT

        if active_zones == self.home_zones:
            return AlarmControlPanelState.ARMED_HOME

        return None

    async def async_alarm_disarm(self, code=None):
        """Disarm the alarm (requires code if configured)."""
        self.check_arm_code(code)
        await self.api.disarm()
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_home(self, code=None):
        """Arm in 'home' mode (requires code if configured)."""
        self.check_arm_code(code)
        await self.__arm_zones(self.home_zones)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_night(self, code=None):
        """Arm in 'night' mode (requires code if configured)."""
        self.check_arm_code(code)
        await self.__arm_zones(self.night_zones)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_away(self, code=None):
        """Arm in 'away' (all zones) mode (requires code if configured)."""
        self.check_arm_code(code)
        await self.api.arm(Zone.ABC)
        await self.coordinator.async_request_refresh()

    def check_arm_code(self, code):
        """Validate the provided arm/disarm code against the configured one."""
        # If no code is configured, do not require one
        if self.arm_code is None:
            return
        if self.arm_code != code:
            raise HomeAssistantError("Invalid code")

    async def __arm_zones(self, int_zones):
        """Send ARM for all zones in the provided bitmask."""
        for zone in int_to_zones(int_zones):
            await self.api.arm(zone)
