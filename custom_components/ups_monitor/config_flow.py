import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_UPS_TYPE, DOMAIN, UPS_TYPE_DUMMY, UPS_TYPE_X1205

_SCHEMA = vol.Schema({
    vol.Required(CONF_UPS_TYPE, default=UPS_TYPE_X1205): SelectSelector(
        SelectSelectorConfig(
            options=[
                {"value": UPS_TYPE_X1205, "label": "X1205 (I2C)"},
                {"value": UPS_TYPE_DUMMY, "label": "Dummy (random values)"},
            ],
            mode=SelectSelectorMode.LIST,
        )
    ),
})


class UpsMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="UPS Monitor", data=user_input)
        return self.async_show_form(step_id="user", data_schema=_SCHEMA)
