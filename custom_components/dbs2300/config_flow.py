import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

class DBS2300ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DBS2300."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return DBS2300OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("device_id"): str,
                vol.Required("local_key"): str,
            }))

        return self.async_create_entry(title="DBS2300", data=user_input)

class DBS2300OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle DBS2300 options."""

    def __init__(self, config_entry):
        """Initialize DBS2300 options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Optional("host", default=self.config_entry.data.get("host")): str,
            vol.Optional("device_id", default=self.config_entry.data.get("device_id")): str,
            vol.Optional("local_key", default=self.config_entry.data.get("local_key")): str,
        }))
