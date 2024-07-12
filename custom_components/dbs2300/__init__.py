import logging
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import tinytuya

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DBS2300 from a config entry."""
    coordinator = DBS2300DataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["sensor", "switch"])
    return True

class DBS2300DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching DBS2300 data."""

    def __init__(self, hass, entry):
        """Initialize."""
        self.hass = hass
        self.entry = entry
        self.device = tinytuya.OutletDevice(entry.data["device_id"], entry.data["host"], entry.data["local_key"])

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_method=self._async_update_data,
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        """Fetch data from DBS2300."""
        try:
            data = await self.hass.async_add_executor_job(self.device.status)
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}")
