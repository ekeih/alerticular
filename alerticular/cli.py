if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
    sys.path.append(parent_dir)

import logging

import click

from alerticular.webhook import run

logging.basicConfig(level=logging.INFO)
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "auto_envvar_prefix": "ALERTICULAR",
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-b",
    "--bot-token",
    "bot_token",
    required=True,
    default=None,
    type=str,
    help="Telegram Bot Token",
)
def cli(bot_token: str = "") -> None:
    run(telegram_token=bot_token)


if __name__ == "__main__":
    cli()
