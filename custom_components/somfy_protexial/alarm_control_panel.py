import logging

from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_DISARMED,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import API, COORDINATOR, DOMAIN
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
    alarms = []
    alarms.append(ProtexialAlarm(coordinator, api))
    async_add_entities(alarms)

class ProtexialAlarm(CoordinatorEntity, AlarmControlPanelEntity):

    def __init__(self, coordinator, api):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.api = api
        self._changed_by = None
        self._attr_state = self.__getCurrentState()

    @property
    def name(self):
        """Return the name of the device."""
        return DEFAULT_ALARM_NAME

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return AlarmControlPanelEntityFeature.ARM_AWAY | AlarmControlPanelEntityFeature.ARM_NIGHT | AlarmControlPanelEntityFeature.ARM_HOME

    @property
    def code_format(self):
        """Return one or more digits/characters."""
        return None

    @property
    def changed_by(self):
        """Return the last change triggered by."""
        return self._changed_by

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_state = self.__getCurrentState()
        self.async_write_ha_state()
        
    def __getCurrentState(self):
        if self.coordinator.data.zoneA == "on" and self.coordinator.data.zoneB == "on" and self.coordinator.data.zoneC == "on":
            return STATE_ALARM_ARMED_AWAY
        elif self.coordinator.data.zoneA == "on" and self.coordinator.data.zoneB == "on":
            return STATE_ALARM_ARMED_NIGHT
        elif self.coordinator.data.zoneA == "on":
            return STATE_ALARM_ARMED_HOME
        else:
            return STATE_ALARM_DISARMED
        
    async def async_alarm_disarm(self, code=None):
        await self.api.disarm()
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_home(self, code=None):
        await self.api.arm(Zone.A)
        await self.coordinator.async_request_refresh()
    
    async def async_alarm_arm_night(self, code=None):
        await self.api.arm(Zone.A)
        await self.api.arm(Zone.B)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_away(self, code=None):
        await self.api.arm(Zone.ABC)
        await self.coordinator.async_request_refresh()
        