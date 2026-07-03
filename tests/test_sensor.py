import pytest
from unittest.mock import MagicMock

from custom_components.ups_monitor.sensor import (
    X1205Battery,
    X1205Voltage,
    X1205Charging,
    async_setup_entry,
)
from custom_components.ups_monitor.const import DOMAIN


@pytest.fixture
def coordinator():
    c = MagicMock()
    c.data = {"battery": 75, "voltage": 3800, "charging": True}
    return c


def test_battery_native_value(coordinator):
    assert X1205Battery(coordinator, "e1").native_value == 75


def test_voltage_native_value(coordinator):
    assert X1205Voltage(coordinator, "e1").native_value == 3800


def test_charging_state_when_charging(coordinator):
    assert X1205Charging(coordinator, "e1").native_value == "charging"


def test_charging_state_when_discharging(coordinator):
    coordinator.data["charging"] = False
    assert X1205Charging(coordinator, "e1").native_value == "discharging"


def test_unique_ids_are_scoped_to_entry_id(coordinator):
    assert X1205Battery(coordinator, "abc")._attr_unique_id == "abc_battery"
    assert X1205Voltage(coordinator, "abc")._attr_unique_id == "abc_voltage"
    assert X1205Charging(coordinator, "abc")._attr_unique_id == "abc_charging"


@pytest.mark.asyncio
async def test_setup_entry_registers_all_three_entities(coordinator):
    hass = MagicMock()
    hass.data = {DOMAIN: {"e1": coordinator}}
    entry = MagicMock()
    entry.entry_id = "e1"

    added = []
    await async_setup_entry(hass, entry, lambda entities: added.extend(entities))

    assert len(added) == 3
    assert any(isinstance(e, X1205Battery) for e in added)
    assert any(isinstance(e, X1205Voltage) for e in added)
    assert any(isinstance(e, X1205Charging) for e in added)
