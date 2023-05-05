"""
Somfy Protexial
"""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    CONF_URL,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API, CONF_CODES, COORDINATOR, DOMAIN
from .protexial import SomfyProtexial

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=20)

PLATFORMS = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.COVER,
    Platform.LIGHT,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    session = aiohttp_client.async_create_clientsession(hass)
    protexial = SomfyProtexial(
        session=session,
        url=entry.data.get(CONF_URL),
        username=entry.data.get(CONF_USERNAME),
        password=entry.data.get(CONF_PASSWORD),
        codes=entry.data.get(CONF_CODES),
    )
    await protexial.init()

    async def _get_status():
        try:
            status = await protexial.get_status()
            _LOGGER.debug(status)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        return status

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Somfy Protexial status update",
        update_method=_get_status,
        update_interval=timedelta(seconds=entry.data.get(CONF_SCAN_INTERVAL)),
    )

    hass.data[DOMAIN][entry.entry_id] = {API: protexial, COORDINATOR: coordinator}

    await coordinator.async_config_entry_first_refresh()

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = hass.data[DOMAIN][entry.entry_id][API]
    await api.logout()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
