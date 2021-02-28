from unittest.mock import MagicMock

import pytest

from alerticular import webhook
from alerticular.target import telegram
from tests.util import get_test_json, get_mock_coro


@pytest.fixture
def cli(loop, aiohttp_client):
    # mock creation and destruction of background tasks
    webhook.on_startup_handler = get_mock_coro(None)
    webhook.on_shutdown_handler = get_mock_coro(None)

    # mock telegram stuff
    telegram.bot = MagicMock()
    telegram.bot.send_message = get_mock_coro(None)
    telegram.dispatcher = MagicMock()

    app = webhook.create_app()
    return loop.run_until_complete(aiohttp_client(app))


async def test_webhook(mocker, cli):
    source = "alertmanager"
    target = "telegram"
    chat = "markusressel"

    alert_data = get_test_json("alertmanager/sample_alert")

    for url in [
        f"/{source}/{target}/{chat}",
        f"/from/{source}/to/{target}/{chat}",
        f"/{source}/to/{chat}/on/{target}",
        f"/{source}/to/{target}/{chat}",
        f"/from/{source}/to/{chat}/on/{target}"
    ]:
        resp = await cli.post(url, json=alert_data)
        assert resp.status == 200
        assert await resp.text() == f"Success: Alerted {chat}."
