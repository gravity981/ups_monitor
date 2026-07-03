from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.ups_monitor.config_flow import UpsMonitorConfigFlow
from custom_components.ups_monitor.const import CONF_UPS_TYPE, DOMAIN, UPS_TYPE_DUMMY, UPS_TYPE_X1205


@pytest.fixture
def flow():
    f = UpsMonitorConfigFlow()
    f.async_set_unique_id = AsyncMock()
    f._abort_if_unique_id_configured = MagicMock()
    f.async_create_entry = MagicMock(
        side_effect=lambda title, data: {"type": "create_entry", "title": title, "data": data}
    )
    f.async_show_form = MagicMock(return_value={"type": "form", "step_id": "user"})
    return f


@pytest.mark.asyncio
async def test_step_user_shows_form_without_input(flow):
    result = await flow.async_step_user(user_input=None)

    flow.async_show_form.assert_called_once()
    assert result["type"] == "form"


@pytest.mark.asyncio
async def test_step_user_creates_entry_on_submit(flow):
    user_input = {CONF_UPS_TYPE: UPS_TYPE_DUMMY}
    await flow.async_step_user(user_input=user_input)

    flow.async_create_entry.assert_called_once_with(title="UPS Monitor", data=user_input)


@pytest.mark.asyncio
async def test_step_user_accepts_x1205_type(flow):
    user_input = {CONF_UPS_TYPE: UPS_TYPE_X1205}
    await flow.async_step_user(user_input=user_input)

    flow.async_create_entry.assert_called_once_with(title="UPS Monitor", data=user_input)


@pytest.mark.asyncio
async def test_step_user_sets_unique_id(flow):
    await flow.async_step_user(user_input=None)

    flow.async_set_unique_id.assert_called_once_with(DOMAIN)


@pytest.mark.asyncio
async def test_step_user_guards_against_duplicate_entry(flow):
    await flow.async_step_user(user_input=None)

    flow._abort_if_unique_id_configured.assert_called_once()
