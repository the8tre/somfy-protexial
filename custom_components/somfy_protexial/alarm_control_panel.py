from functools import reduce
import logging

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    CodeFormat,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_DISARMED,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    API,
    CONF_ARM_CODE,
    CONF_HOME_ZONES,
    CONF_MODES,
    CONF_NIGHT_ZONES,
    COORDINATOR,
    DEVICE_INFO,
    DOMAIN,
    Zone,
)

from .helper import ints_to_zone_array

DEFAULT_ALARM_NAME = "Alarme"
ACTIVATION_ALARM_CODE = None
ALARM_STATE = None

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    modes = config_entry.data.get(CONF_MODES)
    night_zones = config_entry.data.get(CONF_NIGHT_ZONES)
    home_zones = config_entry.data.get(CONF_HOME_ZONES)
    arm_code = config_entry.data.get(CONF_ARM_CODE)
    alarms = []
    alarms.append(
        ProtexialAlarm(
            device_info, coordinator, api, modes, night_zones, home_zones, arm_code
        )
    )
    async_add_entities(alarms)


class ProtexialAlarm(CoordinatorEntity, AlarmControlPanelEntity):
    def __init__(
        self, device_info, coordinator, api, modes, night_zones, home_zones, arm_code
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_control_alarm"
        self._attr_device_info = device_info
        self.coordinator = coordinator
        self.api = api
        self.modes = modes
        self.night_zones = ints_to_zone_array(night_zones)
        self.home_zones = ints_to_zone_array(home_zones)
        self.arm_code = arm_code
        self._changed_by = None
        self._attr_state = self.__getCurrentState()

    @property
    def name(self):
        """Return the name of the device."""
        return DEFAULT_ALARM_NAME

    @property
    def icon(self):
        return "mdi:shield-home"

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return reduce(lambda a, b: a | b, self.modes)

    @property
    def code_format(self):
        """Return one or more digits/characters."""
        if self.arm_code is None:
            return None
        else:
            return CodeFormat.NUMBER

    @property
    def changed_by(self):
        """Return the last change triggered by."""
        return self._changed_by

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_state = self.__getCurrentState()
        self.async_write_ha_state()

    def __getCurrentState(self):
        active_zones = []
        if self.coordinator.data.zoneA == "on":
            active_zones.append(Zone.A)
        if self.coordinator.data.zoneB == "on":
            active_zones.append(Zone.B)
        if self.coordinator.data.zoneC == "on":
            active_zones.append(Zone.C)

        if len(active_zones) == 0:
            return STATE_ALARM_DISARMED

        if len(active_zones) == 3:
            return STATE_ALARM_ARMED_AWAY

        if len(active_zones) == 1:
            if self.night_zones is not None and set(self.night_zones).issubset(
                active_zones
            ):
                return STATE_ALARM_ARMED_NIGHT
            if self.home_zones is not None and set(self.home_zones).issubset(
                active_zones
            ):
                return STATE_ALARM_ARMED_HOME

        if len(active_zones) == 2:
            if self.night_zones is not None and set(active_zones).issubset(
                self.night_zones
            ):
                return STATE_ALARM_ARMED_NIGHT
            if self.home_zones is not None and set(active_zones).issubset(
                self.home_zones
            ):
                return STATE_ALARM_ARMED_HOME

    async def async_alarm_disarm(self, code=None):
        self.check_arm_code(code)
        await self.api.disarm()
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_home(self, code=None):
        self.check_arm_code(code)
        await self.__arm_zones(self.home_zones)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_night(self, code=None):
        self.check_arm_code(code)
        await self.__arm_zones(self.night_zones)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_away(self, code=None):
        self.check_arm_code(code)
        await self.api.arm(Zone.ABC)
        await self.coordinator.async_request_refresh()

    def check_arm_code(self, code):
        if not self.arm_code == code:
            raise HomeAssistantError("Invalid code")

    async def __arm_zones(self, zones):
        for zone in zones:
            await self.api.arm(Zone(zone))
