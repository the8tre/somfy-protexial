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
    night_zones = config_entry.data.get(CONF_NIGHT_ZONES)
    home_zones = config_entry.data.get(CONF_HOME_ZONES)
    arm_code = config_entry.data.get(CONF_ARM_CODE)
    alarms = []
    alarms.append(
        ProtexialAlarm(device_info, coordinator, api, night_zones, home_zones, arm_code)
    )
    async_add_entities(alarms)


class ProtexialAlarm(CoordinatorEntity, AlarmControlPanelEntity):
    def __init__(
        self, device_info, coordinator, api, night_zones, home_zones, arm_code
    ) -> None:
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
    def code_arm_required(self) -> bool:
        """Whether the code is required for arm actions."""
        return self.arm_code is not None

    @property
    def changed_by(self):
        """Return the last change triggered by."""
        return self._changed_by

    @property
    def alarm_state(self) -> AlarmControlPanelState | None:
        """Return the state of the alarm."""
        return self.__getCurrentState()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if (
            self.coordinator.data.zone_a is None
            or self.coordinator.data.zone_b is None
            or self.coordinator.data.zone_c is None
        ):
            return False
        return super().available

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    def __getCurrentState(self) -> AlarmControlPanelState | None:
        active_zones = Zone.NONE.value
        if self.coordinator.data.zone_a == "on":
            active_zones += Zone.A.value
        if self.coordinator.data.zone_b == "on":
            active_zones += Zone.B.value
        if self.coordinator.data.zone_c == "on":
            active_zones += Zone.C.value

        if active_zones == Zone.NONE.value:
            return AlarmControlPanelState.DISARMED

        if active_zones == Zone.ABC.value:
            return AlarmControlPanelState.ARMED_AWAY

        if active_zones == self.night_zones:
            return AlarmControlPanelState.ARMED_NIGHT

        if active_zones == self.home_zones:
            return AlarmControlPanelState.ARMED_HOME

        return None

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

    async def __arm_zones(self, int_zones):
        for zone in int_to_zones(int_zones):
            await self.api.arm(zone)
