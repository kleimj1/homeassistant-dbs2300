import logging
from homeassistant.helpers import discovery
from homeassistant.const import CONF_HOST, CONF_DEVICE_ID, CONF_API_KEY

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the DBS2300 component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, entry):
    """Set up DBS2300 from a config entry."""
    data = entry.data

    host = data[CONF_HOST]
    device_id = data[CONF_DEVICE_ID]
    local_key = data.get(CONF_API_KEY)

    if data.get("use_secrets"):
        local_key = hass.secrets.get(local_key, local_key)

    hass.data[DOMAIN][entry.entry_id] = {
        CONF_HOST: host,
        CONF_DEVICE_ID: device_id,
        CONF_API_KEY: local_key
    }

    for component in ("sensor", "switch"):
        hass.async_create_task(
            discovery.async_load_platform(hass, component, DOMAIN, {}, entry.data)
        )

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    return True
