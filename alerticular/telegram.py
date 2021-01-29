import logging
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.utils.emoji import emojize
from jinja2 import Environment, PackageLoader

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
    dispatcher.register_message_handler(echo)


async def run() -> None:
    logger.info("Starting Telegram bot")
    await dispatcher.start_polling()


async def send_welcome(message: types.Message) -> None:
    logger.info("{}: {}".format(message.chat, message.text))
    await message.reply(
        "This bot is alerticular good!\nYour chat ID is: `{}`".format(message.chat.id), parse_mode="Markdown"
    )


async def echo(message: types.Message) -> None:
    logger.info("{}: {}".format(message.chat, message.text))
    await message.answer("Echo: {}".format(message.text))


async def send_alert(chat: str, alert: JSONType) -> None:
    message = await alertmanager_template.render_async(alert)

    # check if the chat variable is an integer or a string
    # if it is an integer, its a chat ID and we are done
    # if it is a string, it is probably a username or channel,
    #   so we prefix it with an "@" symbol to let aiogram know
    try:
        int(chat)
    except:
        if not chat.startswith("@"):
            chat = f"@{chat}"

    await bot.send_message(chat, emojize(message), parse_mode="Markdown", disable_web_page_preview=True)
