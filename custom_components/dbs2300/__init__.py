"""DBS2300 component setup."""
import logging
from homeassistant.helpers import discovery
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the DBS2300 component."""
    conf = config[DOMAIN]
    hass.data[DOMAIN] = {
        'host': conf['host'],
        'device_id': conf['device_id'],
        'local_key': conf['local_key']
    }
    
    discovery.load_platform(hass, 'sensor', DOMAIN, {}, config)
    discovery.load_platform(hass, 'switch', DOMAIN, {}, config)
    
    return True
