from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the DBS2300 component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, entry):
    """Set up DBS2300 from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    for component in ("sensor", "switch"):
        hass.async_create_task(
            discovery.async_load_platform(hass, component, DOMAIN, {}, entry.data)
        )

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
