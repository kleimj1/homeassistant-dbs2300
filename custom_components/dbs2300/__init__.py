import asyncio
import logging
import async_timeout

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

PLATFORMS = ["sensor", "switch"]

async def async_setup_entry(hass, entry):
    """Set up DBS2300 from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = DBS2300DataUpdateCoordinator(
        hass, entry.data
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    entry.add_update_listener(async_reload_entry)
    return True

class DBS2300DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching DBS2300 data."""

    def __init__(self, hass, config):
        """Initialize."""
        self.config = config
        self.api = DBS2300API(config)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                return await self.api.get_data()
        except Exception as error:
            raise UpdateFailed(f"Error communicating with API: {error}")

async def async_reload_entry(hass, entry):
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
