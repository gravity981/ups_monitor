from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.ups_monitor.const import UPS_TYPE_DUMMY, UPS_TYPE_X1205
from custom_components.ups_monitor.coordinator import (
    DummyClient,
    X1205Client,
    _create_client,
    async_setup_coordinator,
)

# --- DummyClient ---


def test_dummy_client_returns_required_keys():
    assert set(DummyClient().read_all()) == {"battery", "voltage", "charging"}


def test_dummy_client_battery_in_range():
    client = DummyClient()
    for _ in range(20):
        assert 0 <= client.read_all()["battery"] <= 100


def test_dummy_client_voltage_in_range():
    client = DummyClient()
    for _ in range(20):
        assert 3000 <= client.read_all()["voltage"] <= 4200


def test_dummy_client_charging_is_bool():
    assert isinstance(DummyClient().read_all()["charging"], bool)


# --- X1205Client ---


@pytest.fixture
def mock_bus():
    with patch("custom_components.ups_monitor.coordinator.SMBus") as mock_cls:
        bus = MagicMock()
        mock_cls.return_value = bus
        yield bus


def test_x1205_opens_correct_i2c_bus():
    with patch("custom_components.ups_monitor.coordinator.SMBus") as mock_cls:
        mock_cls.return_value = MagicMock()
        X1205Client()
        mock_cls.assert_called_once_with(1)


def test_x1205_client_maps_register_values(mock_bus):
    mock_bus.read_byte_data.side_effect = lambda addr, reg: {0x04: 85, 0x01: 0x40}.get(reg, 0)
    mock_bus.read_word_data.return_value = 3900

    data = X1205Client().read_all()

    assert data["battery"] == 85
    assert data["voltage"] == 3900
    assert data["charging"] is True


def test_x1205_client_charging_false_when_flag_clear(mock_bus):
    mock_bus.read_byte_data.side_effect = lambda addr, reg: {0x04: 50, 0x01: 0x00}.get(reg, 0)
    mock_bus.read_word_data.return_value = 3500

    assert X1205Client().read_all()["charging"] is False


# --- _create_client ---


def test_create_client_returns_dummy(mock_bus):
    assert isinstance(_create_client(UPS_TYPE_DUMMY), DummyClient)


def test_create_client_returns_x1205(mock_bus):
    assert isinstance(_create_client(UPS_TYPE_X1205), X1205Client)


def test_create_client_raises_for_unknown_type():
    with pytest.raises(ValueError, match="Unknown UPS type"):
        _create_client("not_a_real_type")


# --- async_setup_coordinator ---


@pytest.mark.asyncio
async def test_coordinator_data_populated_after_first_refresh():
    expected = {"battery": 60, "voltage": 3700, "charging": False}
    mock_hass = MagicMock()
    mock_hass.async_add_executor_job = AsyncMock(return_value=expected)

    coordinator = await async_setup_coordinator(mock_hass, UPS_TYPE_DUMMY)

    assert coordinator.data == expected


@pytest.mark.asyncio
async def test_coordinator_runs_io_in_executor():
    mock_hass = MagicMock()
    mock_hass.async_add_executor_job = AsyncMock(return_value={"battery": 50, "voltage": 3600, "charging": True})

    await async_setup_coordinator(mock_hass, UPS_TYPE_DUMMY)

    mock_hass.async_add_executor_job.assert_called_once()
