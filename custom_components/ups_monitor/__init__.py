import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_UPS_TYPE, DOMAIN
from .coordinator import async_setup_coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ups_type = entry.data[CONF_UPS_TYPE]
    _LOGGER.debug("Setting up entry %s with UPS type '%s'", entry.entry_id, ups_type)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = await async_setup_coordinator(hass, ups_type)
    _LOGGER.debug("Coordinator ready, forwarding setup to platforms: %s", PLATFORMS)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("Entry %s setup complete", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading entry %s", entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    _LOGGER.debug("Entry %s unloaded (ok=%s)", entry.entry_id, unload_ok)
    return unload_ok
