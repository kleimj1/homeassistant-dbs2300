"""Platform for sensor integration."""
from homeassistant.helpers.entity import Entity
import tinytuya
from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    host = hass.data[DOMAIN]['host']
    device_id = hass.data[DOMAIN]['device_id']
    local_key = hass.data[DOMAIN]['local_key']
    
    sensors = []
    sensors.append(DBS2300Sensor(host, device_id, local_key))
    async_add_entities(sensors, True)

class DBS2300Sensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, host, device_id, local_key):
        """Initialize the sensor."""
        self._state = None
        self._name = "DBS2300 Sensor"
        self.device = tinytuya.OutletDevice(device_id, host, local_key)
        self.device.set_version(3.3)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        status = self.device.status()
        self._state = status['dps']['1']  # Beispiel: Status des AC Output Power
