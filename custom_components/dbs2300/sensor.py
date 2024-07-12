import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the DBS2300 sensors."""
    if discovery_info is None:
        return

    host = discovery_info["host"]
    device_id = discovery_info["device_id"]
    local_key = discovery_info["local_key"]

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(Dbs2300Sensor(host, device_id, local_key, sensor_type))

    async_add_entities(entities)

class Dbs2300Sensor(SensorEntity):
    """Representation of a DBS2300 sensor."""

    def __init__(self, host, device_id, local_key, sensor_type):
        """Initialize the sensor."""
        self._host = host
        self._device_id = device_id
        self._local_key = local_key
        self._sensor_type = sensor_type
        self._name = SENSOR_TYPES[sensor_type]
        self._state = None

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
        import tinytuya
        device = tinytuya.OutletDevice(self._device_id, self._host, self._local_key)
        data = device.status()

        if data:
            self._state = data.get(self._sensor_type)
