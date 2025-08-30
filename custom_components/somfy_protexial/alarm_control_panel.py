import logging
from dataclasses import dataclass
from functools import reduce

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityDescription,
)
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
    CodeFormat,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.somfy_protexial.protexial_entity import (
    ProtexialBaseEntity,
    ProtexialEntityDescription,
)

from .const import (
    API,
    CONF_ARM_CODE,
    CONF_HOME_ZONES,
    CONF_NIGHT_ZONES,
    COORDINATOR,
    DOMAIN,
    Zone,
)
from .helper import int_to_zones

DEFAULT_ALARM_NAME = "Alarme"
ACTIVATION_ALARM_CODE = None
ALARM_STATE = None

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class ProtexialAlarmControlPanelEntityDescription(
    ProtexialEntityDescription, AlarmControlPanelEntityDescription
):
    """Describes Alarm Control Panel entity."""


ALARM_CONTROL_PANEL_DESCRIPTION = ProtexialAlarmControlPanelEntityDescription(
    key="alarm",
    translation_key="alarm",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    api = hass.data[DOMAIN][config_entry.entry_id][API]
    night_zones = config_entry.data.get(CONF_NIGHT_ZONES)
    home_zones = config_entry.data.get(CONF_HOME_ZONES)
    arm_code = config_entry.data.get(CONF_ARM_CODE)
    alarms = []
    alarms.append(
        ProtexialAlarm(
            coordinator,
            config_entry,
            ALARM_CONTROL_PANEL_DESCRIPTION,
            api,
            night_zones,
            home_zones,
            arm_code,
        )
    )
    async_add_entities(alarms)


class ProtexialAlarm(ProtexialBaseEntity, AlarmControlPanelEntity):
    def __init__(
        self,
        coordinator,
        config_entry,
        description,
        api,
        night_zones,
        home_zones,
        arm_code,
    ) -> None:
        super().__init__(coordinator, config_entry, description)
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
