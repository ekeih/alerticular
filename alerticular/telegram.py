import logging
from aiogram import Bot, Dispatcher, executor, types


class Telegram:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher(self.bot)
        self.dispatcher.register_message_handler(self.send_welcome, commands=["start", "help"])
        self.dispatcher.register_message_handler(self.echo)

    async def send_welcome(self, message: types.Message):
        logging.info("{}: {}".format(message.chat, message.text))
        await message.reply("This bot is alerticular good!")

    async def echo(self, message: types.Message):
        logging.info("{}: {}".format(message.chat, message.text))
        await message.answer("Echo: {}".format(message.text))

    async def run(self):
        logging.info("Starting Telegram bot")
        await self.dispatcher.start_polling()
