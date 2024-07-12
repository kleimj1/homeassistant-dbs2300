import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the DBS2300 sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []

    for sensor_type in SENSOR_TYPES:
        sensors.append(Dbs2300Sensor(coordinator, sensor_type))

    async_add_entities(sensors)

class Dbs2300Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a DBS2300 sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._name = SENSOR_TYPES[sensor_type]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.coordinator.entry.data['device_id']}_{self._sensor_type}"

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "last_updated": self.coordinator.data.get("last_updated"),
        }
