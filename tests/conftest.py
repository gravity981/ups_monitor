"""
Minimal stubs for homeassistant modules so tests run without the full HA package.

The tricky case is `from homeassistant import config_entries` in config_flow.py.
Python resolves that by calling getattr() on the top-level homeassistant mock
rather than looking up sys.modules['homeassistant.config_entries'], so we must
set the attribute explicitly on the homeassistant mock object.
"""
import sys
from unittest.mock import MagicMock


class _ConfigFlow:
    """Absorbs the `domain=` keyword that HA's real metaclass would handle."""
    @classmethod
    def __init_subclass__(cls, domain=None, **kwargs):
        super().__init_subclass__(**kwargs)


class _CoordinatorEntity:
    def __init__(self, coordinator):
        self.coordinator = coordinator


class _SensorEntity:
    pass


class _SensorDeviceClass:
    BATTERY = "battery"
    VOLTAGE = "voltage"
    ENUM = "enum"


class _SensorStateClass:
    MEASUREMENT = "measurement"


class _UnitOfElectricPotential:
    MILLIVOLT = "mV"
    VOLT = "V"


class _FakeDataUpdateCoordinator:
    def __init__(self, hass, logger, name, update_interval, update_method):
        self._update_method = update_method
        self.data = None

    async def async_config_entry_first_refresh(self):
        self.data = await self._update_method()


_config_entries = MagicMock()
_config_entries.ConfigFlow = _ConfigFlow

_ha_coordinator = MagicMock()
_ha_coordinator.DataUpdateCoordinator = _FakeDataUpdateCoordinator
_ha_coordinator.CoordinatorEntity = _CoordinatorEntity

_ha_sensor = MagicMock()
_ha_sensor.SensorEntity = _SensorEntity
_ha_sensor.SensorDeviceClass = _SensorDeviceClass
_ha_sensor.SensorStateClass = _SensorStateClass

_ha_const = MagicMock()
_ha_const.PERCENTAGE = "%"
_ha_const.UnitOfElectricPotential = _UnitOfElectricPotential

# Top-level homeassistant mock must have config_entries set as an attribute so
# that `from homeassistant import config_entries` resolves to our stub rather
# than an auto-generated MagicMock attribute.
_homeassistant = MagicMock()
_homeassistant.config_entries = _config_entries

for _name, _mod in {
    "homeassistant": _homeassistant,
    "homeassistant.config_entries": _config_entries,
    "homeassistant.core": MagicMock(),
    "homeassistant.helpers": MagicMock(),
    "homeassistant.helpers.update_coordinator": _ha_coordinator,
    "homeassistant.helpers.selector": MagicMock(),
    "homeassistant.components": MagicMock(),
    "homeassistant.components.sensor": _ha_sensor,
    "homeassistant.const": _ha_const,
    "voluptuous": MagicMock(),
}.items():
    sys.modules[_name] = _mod
