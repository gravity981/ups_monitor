from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.ups_monitor import async_setup_entry, async_unload_entry
from custom_components.ups_monitor.const import DOMAIN, UPS_TYPE_DUMMY


@pytest.fixture
def hass():
    h = MagicMock()
    h.data = {}
    h.config_entries.async_forward_entry_setups = AsyncMock()
    h.config_entries.async_unload_platforms = AsyncMock(return_value=True)
    return h


@pytest.fixture
def entry():
    e = MagicMock()
    e.entry_id = "test_id"
    e.data = {"ups_type": UPS_TYPE_DUMMY}
    return e


@pytest.mark.asyncio
async def test_setup_entry_stores_coordinator(hass, entry):
    mock_coordinator = MagicMock()
    with patch(
        "custom_components.ups_monitor.async_setup_coordinator",
        AsyncMock(return_value=mock_coordinator),
    ):
        await async_setup_entry(hass, entry)

    assert hass.data[DOMAIN][entry.entry_id] is mock_coordinator


@pytest.mark.asyncio
async def test_setup_entry_forwards_to_sensor_platform(hass, entry):
    with patch(
        "custom_components.ups_monitor.async_setup_coordinator",
        AsyncMock(return_value=MagicMock()),
    ):
        result = await async_setup_entry(hass, entry)

    hass.config_entries.async_forward_entry_setups.assert_called_once_with(entry, ["sensor"])
    assert result is True


@pytest.mark.asyncio
async def test_unload_entry_removes_coordinator(hass, entry):
    hass.data = {DOMAIN: {entry.entry_id: MagicMock()}}

    await async_unload_entry(hass, entry)

    assert entry.entry_id not in hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_unload_entry_returns_platform_result(hass, entry):
    hass.data = {DOMAIN: {entry.entry_id: MagicMock()}}
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

    result = await async_unload_entry(hass, entry)

    assert result is True
