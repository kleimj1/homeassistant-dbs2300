import logging
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Dabbsson DBS2300 switches."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    entities = [
        DabbssonSwitch(config, "AC Output Control", "ac_output_control"),
    ]
    async_add_entities(entities, True)

class DabbssonSwitch(SwitchEntity):
    """Representation of a Dabbsson DBS2300 switch."""

    def __init__(self, config, name, switch_type):
        self._config = config
        self._name = name
        self._type = switch_type
        self._state = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        # Hier die tinytuya Logik zum Einschalten der AC-Ausgangsleistung einfügen
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        # Hier die tinytuya Logik zum Ausschalten der AC-Ausgangsleistung einfügen
        self._state = False
        self.schedule_update_ha_state()
