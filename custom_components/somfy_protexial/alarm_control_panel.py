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

from .const import API, CONF_ARM_CODE, CONF_MODES, COORDINATOR, DOMAIN
from .protexial import Zone

DEFAULT_ALARM_NAME = "Somfy Protexial"
ACTIVATION_ALARM_CODE = None
ALARM_STATE = None

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    modes = config_entry.data.get(CONF_MODES)
    arm_code = config_entry.data.get(CONF_ARM_CODE)
    alarms = []
    alarms.append(ProtexialAlarm(coordinator, api, modes, arm_code))
    async_add_entities(alarms)


class ProtexialAlarm(CoordinatorEntity, AlarmControlPanelEntity):
    def __init__(self, coordinator, api, modes, arm_code):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.api = api
        self.modes = modes
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
        if (
            self.coordinator.data.zoneA == "on"
            and self.coordinator.data.zoneB == "on"
            and self.coordinator.data.zoneC == "on"
        ):
            return STATE_ALARM_ARMED_AWAY
        elif (
            self.coordinator.data.zoneA == "on" and self.coordinator.data.zoneB == "on"
        ):
            return STATE_ALARM_ARMED_NIGHT
        elif self.coordinator.data.zoneA == "on":
            return STATE_ALARM_ARMED_HOME
        else:
            return STATE_ALARM_DISARMED

    async def async_alarm_disarm(self, code=None):
        self.check_arm_code(code)
        await self.api.disarm()
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_home(self, code=None):
        self.check_arm_code(code)
        await self.api.arm(Zone.A)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_night(self, code=None):
        self.check_arm_code(code)
        await self.api.arm(Zone.A)
        await self.api.arm(Zone.B)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_away(self, code=None):
        self.check_arm_code(code)
        await self.api.arm(Zone.ABC)
        await self.coordinator.async_request_refresh()

    def check_arm_code(self, code):
        if not self.arm_code == code:
            raise HomeAssistantError('Invalid code')
