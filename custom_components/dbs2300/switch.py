"""Platform for switch integration."""
from homeassistant.components.switch import SwitchEntity
import tinytuya
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the switch platform."""
    host = hass.data[DOMAIN]['host']
    device_id = hass.data[DOMAIN]['device_id']
    local_key = hass.data[DOMAIN]['local_key']
    
    switches = []
    switches.append(DBS2300Switch(host, device_id, local_key))
    async_add_entities(switches, True)

class DBS2300Switch(SwitchEntity):
    """Representation of a Switch."""

    def __init__(self, host, device_id, local_key):
        """Initialize the switch."""
        self._state = False
        self._name = "DBS2300 Switch"
        self.device = tinytuya.OutletDevice(device_id, host, local_key)
        self.device.set_version(3.3)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        self.device.set_status(True, '1')  # Beispiel: Schaltet AC Output Power ein
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        self.device.set_status(False, '1')  # Beispiel: Schaltet AC Output Power aus
        self._state = False

    async def async_update(self):
        """Fetch new state data for the switch."""
        status = self.device.status()
        self._state = status['dps']['1']
