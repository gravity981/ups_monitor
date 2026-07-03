import logging

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
import voluptuous as vol

from .const import CONF_UPS_TYPE, DOMAIN, UPS_TYPE_DUMMY, UPS_TYPE_X1205

_LOGGER = logging.getLogger(__name__)

_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_UPS_TYPE, default=UPS_TYPE_X1205): SelectSelector(
            SelectSelectorConfig(
                options=[
                    {"value": UPS_TYPE_X1205, "label": "X1205 (I2C)"},
                    {"value": UPS_TYPE_DUMMY, "label": "Dummy (random values)"},
                ],
                mode=SelectSelectorMode.LIST,
            )
        ),
    }
)


class UpsMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("Config flow step 'user', input: %s", user_input)
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            _LOGGER.debug("Creating config entry with data: %s", user_input)
            return self.async_create_entry(title="UPS Monitor", data=user_input)
        return self.async_show_form(step_id="user", data_schema=_SCHEMA)
