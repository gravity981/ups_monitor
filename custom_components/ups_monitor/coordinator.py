import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from smbus2 import SMBus

_LOGGER = logging.getLogger(__name__)

I2C_BUS = 1
I2C_ADDRESS = 0x36


class X1205Client:
    def __init__(self):
        self.bus = SMBus(I2C_BUS)

    def read_all(self):
        # NOTE: adjust registers based on X1205 docs
        return {
            "battery": self.bus.read_byte_data(I2C_ADDRESS, 0x04),
            "voltage": self.bus.read_word_data(I2C_ADDRESS, 0x02),
            "charging": bool(self.bus.read_byte_data(I2C_ADDRESS, 0x01) & 0x40),
        }


async def async_setup_coordinator(hass):
    client = X1205Client()

    async def _async_update():
        return await hass.async_add_executor_job(client.read_all)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="x1205_ups",
        update_interval=timedelta(seconds=30),
        update_method=_async_update,
    )

    await coordinator.async_config_entry_first_refresh()

    return coordinator
