import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Dabbsson DBS2300 sensors."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    entities = [
        DabbssonSensor(config, "AC Output Power", "ac_output_power"),
        DabbssonSensor(config, "DC Output Power", "dc_output_power"),
        DabbssonSensor(config, "Battery Capacity", "battery_capacity"),
    ]
    async_add_entities(entities, True)

class DabbssonSensor(Entity):
    """Representation of a Dabbsson DBS2300 sensor."""

    def __init__(self, config, name, sensor_type):
        self._config = config
        self._name = name
        self._type = sensor_type
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        # Hier die tinytuya Logik zum Abrufen der Sensorwerte einfügen
        pass
