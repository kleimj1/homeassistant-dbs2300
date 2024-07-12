import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class Dbs2300FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dbs2300."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            if user_input.get('use_secrets'):
                if all(user_input[key] for key in ("host", "device_id")):
                    return self.async_create_entry(title="DBS2300", data=user_input)
                else:
                    errors["base"] = "missing_data"
            else:
                if all(user_input[key] for key in ("host", "device_id", "local_key")):
                    return self.async_create_entry(title="DBS2300", data=user_input)
                else:
                    errors["base"] = "missing_data"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host"): str,
                    vol.Required("device_id"): str,
                    vol.Optional("local_key"): str,
                    vol.Optional("use_secrets", default=False): bool,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return Dbs2300OptionsFlowHandler(config_entry)


class Dbs2300OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Dbs2300."""

    def __init__(self, config_entry):
        """Initialize Dbs2300 options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the user options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host", default=self.config_entry.options.get("host", "")): str,
                    vol.Required("device_id", default=self.config_entry.options.get("device_id", "")): str,
                    vol.Optional("local_key", default=self.config_entry.options.get("local_key", "")): str,
                    vol.Optional("use_secrets", default=self.config_entry.options.get("use_secrets", False)): bool,
                }
            ),
        )
