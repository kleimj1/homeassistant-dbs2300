import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SWITCH_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the DBS2300 switches."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = []

    for switch_type in SWITCH_TYPES:
        switches.append(Dbs2300Switch(coordinator, switch_type))

    async_add_entities(switches)

class Dbs2300Switch(CoordinatorEntity, SwitchEntity):
    """Representation of a DBS2300 switch."""

    def __init__(self, coordinator, switch_type):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._switch_type = switch_type
        self._name = SWITCH_TYPES[switch_type]

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.coordinator.data.get(self._switch_type) == "ON"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.coordinator.entry.data['device_id']}_{self._switch_type}"

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.hass.async_add_executor_job(self.coordinator.device.turn_on, self._switch_type)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.hass.async_add_executor_job(self.coordinator.device.turn_off, self._switch_type)
        await self.coordinator.async_request_refresh()
