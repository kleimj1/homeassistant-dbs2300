import logging
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN, SWITCH_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the DBS2300 switches."""
    if discovery_info is None:
        return

    host = discovery_info["host"]
    device_id = discovery_info["device_id"]
    local_key = discovery_info["local_key"]

    entities = []
    for switch_type in SWITCH_TYPES:
        entities.append(Dbs2300Switch(host, device_id, local_key, switch_type))

    async_add_entities(entities)

class Dbs2300Switch(SwitchEntity):
    """Representation of a DBS2300 switch."""

    def __init__(self, host, device_id, local_key, switch_type):
        """Initialize the switch."""
        self._host = host
        self._device_id = device_id
        self._local_key = local_key
        self._switch_type = switch_type
        self._name = SWITCH_TYPES[switch_type]
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        import tinytuya
        device = tinytuya.OutletDevice(self._device_id, self._host, self._local_key)
        device.set_status(True, self._switch_type)
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        import tinytuya
        device = tinytuya.OutletDevice(self._device_id, self._host, self._local_key)
        device.set_status(False, self._switch_type)
        self._state = False
