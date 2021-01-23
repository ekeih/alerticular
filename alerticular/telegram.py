import logging
from typing import Dict, Any
from jinja2 import Environment, PackageLoader
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.emoji import emojize


logger = logging.getLogger(__name__)
JSONType = Dict[str, Any]

bot = None
dispatcher = None

jinja2_environment = Environment(
    loader=PackageLoader("alerticular", "templates"), enable_async=True, trim_blocks=True, lstrip_blocks=True
)
alertmanager_template = jinja2_environment.get_template("alertmanager.md")


def setup(token: str):
    global bot
    global dispatcher
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot)
    dispatcher.register_message_handler(send_welcome, commands=["start", "help"])
    dispatcher.register_message_handler(echo)


async def run():
    logger.info("Starting Telegram bot")
    await dispatcher.start_polling()


async def send_welcome(message: types.Message):
    logger.info("{}: {}".format(message.chat, message.text))
    await message.reply(
        "This bot is alerticular good!\nYour chat ID is: `{}`".format(message.chat.id), parse_mode="Markdown"
    )


async def echo(message: types.Message):
    logger.info("{}: {}".format(message.chat, message.text))
    await message.answer("Echo: {}".format(message.text))


async def send_alert(chat: str, alert: JSONType):
    message = await alertmanager_template.render_async(alert)
    await bot.send_message(chat, emojize(message), parse_mode="Markdown", disable_web_page_preview=True)
