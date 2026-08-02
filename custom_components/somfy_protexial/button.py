# Buttons (default/error acknowledgement: battery, alarm, radio link)
#
# These buttons let the user acknowledge/reset the 3 "defaut" flags exposed
# by status.xml (defaut0/battery, defaut1/radio link, defaut3/alarm) without
# having to walk to the centrale. They are based on the Jeedom protexiom
# plugin's "EraseDefault" commands (RESET_BATTERY_ERR / RESET_ALARM_ERR /
# RESET_LINK_ERR in phpProtexiom.class.php), which POST a small form to the
# elements list page (u_listelmt.htm).
import logging
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import API, BUTTONS, DEVICE_INFO, DOMAIN
from .somfy_exception import SomfyException

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform (default reset buttons)."""
    protexial = hass.data[DOMAIN][config_entry.entry_id][API]
    device_info = hass.data[DOMAIN][config_entry.entry_id][DEVICE_INFO]

    entities = []
    for button in BUTTONS:
        description = ButtonEntityDescription(
            key=button["id"],
            translation_key=button["translation_key"],
            icon=button.get("icon"),
            entity_category=EntityCategory.CONFIG,
        )
        entities.append(ProtexialResetButton(device_info, protexial, description))

    if entities:
        async_add_entities(entities)
    else:
        _LOGGER.debug("No buttons to add.")


class ProtexialResetButton(ButtonEntity):
    """Button that acknowledges/resets one of the centrale's default flags."""

    _attr_has_entity_name = True

    def __init__(
        self, device_info, protexial, description: ButtonEntityDescription
    ) -> None:
        """Initialize a translated reset button."""
        self.entity_description = description
        self._attr_translation_key = description.translation_key
        self._protexial = protexial
        self._button_id = description.key
        self._attr_unique_id = f"{DOMAIN}_{self._button_id}"
        self._attr_device_info = device_info

    async def async_press(self) -> None:
        """Call the matching reset_xxx() coroutine on the API client."""
        method = getattr(self._protexial, self._button_id, None)
        if method is None:
            _LOGGER.error(
                "No API method found for button '%s'", self._button_id
            )
            return
        try:
            await method()
        except SomfyException as ex:
            _LOGGER.error(
                "Failed to reset default '%s': %s", self._button_id, ex
            )
            raise
