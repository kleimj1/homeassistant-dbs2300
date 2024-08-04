import logging
import asyncio
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import tinytuya

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Richte DBS2300 aus einem Konfigurationseintrag ein."""
    coordinator = DBS2300DataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "switch"])
    return True

class DBS2300DataUpdateCoordinator(DataUpdateCoordinator):
    """Klasse zur Verwaltung der Datenaktualisierung von DBS2300."""

    def __init__(self, hass, entry):
        """Initialisierung."""
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
        """Daten von DBS2300 abrufen."""
        try:
            data = await self.hass.async_add_executor_job(self.device.status)
            return data
        except Exception as err:
            raise UpdateFailed(f"Fehler bei der Kommunikation mit dem Gerät: {err}")
