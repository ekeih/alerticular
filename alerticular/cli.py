import asyncio
import logging
import click
from alerticular.webhook import run


logging.basicConfig(level=logging.INFO)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-b", "--bot-token", "bot_token", default=None, type=str, help="Telegram Bot Token")
def cli(bot_token: str):
    run(telegram_token=bot_token)
