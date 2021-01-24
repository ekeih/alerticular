import logging
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.utils.emoji import emojize
from jinja2 import Environment, PackageLoader
from telegram_click_aio.decorator import command

from alerticular import alertmanager

logger = logging.getLogger(__name__)
JSONType = Dict[str, Any]

bot: Bot = None
dispatcher: Dispatcher = None

jinja2_environment = Environment(
    loader=PackageLoader("alerticular", "templates"), enable_async=True, trim_blocks=True, lstrip_blocks=True
)
alertmanager_template = jinja2_environment.get_template("alertmanager.md")


def setup(token: str) -> None:
    global bot
    global dispatcher
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot)
    dispatcher.register_message_handler(send_welcome, commands=["start", "help"])
    dispatcher.register_message_handler(handle_alerts, commands=["alerts", "a"])
    dispatcher.register_message_handler(echo)


async def run() -> None:
    logger.info("Starting Telegram bot")
    await dispatcher.start_polling()


async def send_welcome(message: types.Message) -> None:
    logger.info("{}: {}".format(message.chat, message.text))
    await message.reply(
        "This bot is alerticular good!\nYour chat ID is: `{}`".format(message.chat.id), parse_mode="Markdown"
    )


@command(name=["alerts", "a"], description='Show a list of all alerts.')
async def handle_alerts(message: types.Message) -> None:
    logger.info("{}: {}".format(message.chat, message.text))
    alerts = await alertmanager.get_alerts()
    lines = []
    for alert in alerts:
        alert_name = alert.get("labels", {}).get("alertname", None)
        alert_message = alert.get("annotations", {}).get("message", None)
        if alert_name is not None:
            lines.append(f":fire: {alert_name}: {alert_message}")
    text = "\n".join(lines).strip()
    if len(text) <= 0:
        text = "No alerts right now"
    await message.reply(emojize(text), parse_mode="Markdown", disable_web_page_preview=True)


async def echo(message: types.Message) -> None:
    logger.info("{}: {}".format(message.chat, message.text))
    await message.answer("Echo: {}".format(message.text))


async def send_alert(chat: str, alert: JSONType) -> None:
    message = await alertmanager_template.render_async(alert)
    await bot.send_message(chat, emojize(message), parse_mode="Markdown", disable_web_page_preview=True)
