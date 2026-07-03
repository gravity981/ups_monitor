import logging
import random
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from smbus2 import SMBus

from .const import UPS_TYPE_DUMMY, UPS_TYPE_X1205

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


class DummyClient:
    def read_all(self):
        return {
            "battery": random.randint(0, 100),
            "voltage": random.randint(3000, 4200),
            "charging": random.choice([True, False]),
        }


def _create_client(ups_type):
    if ups_type == UPS_TYPE_DUMMY:
        return DummyClient()
    if ups_type == UPS_TYPE_X1205:
        return X1205Client()
    raise ValueError(f"Unknown UPS type: {ups_type}")


async def async_setup_coordinator(hass, ups_type):
    client = _create_client(ups_type)

    async def _async_update():
        return await hass.async_add_executor_job(client.read_all)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ups_monitor",
        update_interval=timedelta(seconds=30),
        update_method=_async_update,
    )

    await coordinator.async_config_entry_first_refresh()

    return coordinator
