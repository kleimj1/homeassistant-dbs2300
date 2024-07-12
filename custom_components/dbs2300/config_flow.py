import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

class DabbssonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dabbsson DBS2300."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLLING

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Dabbsson DBS2300", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("device_id"): str,
            vol.Required("local_key"): str,
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)
