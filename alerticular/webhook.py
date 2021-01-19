import asyncio
from aiohttp import web
import logging
from alerticular.telegram import Telegram
from alerticular.metrics import run_metrics_endpoint

routes = web.RouteTableDef()


@routes.get("/")
async def handle(request):
    return web.Response(text="Hello World!")


@routes.get("/out/telegram/{chat}/spam")
async def spam(request):
    chat = request.match_info.get("chat")
    await request.app["telegram_bot"].bot.send_message(chat, "Spam, Spam, Spam!")
    return web.Response(text="Success: {} got spammed".format(chat))


async def start_background_tasks(app):
    logging.info("Adding background tasks")
    app["metrics"] = asyncio.create_task(run_metrics_endpoint())
    app["telegram"] = asyncio.create_task(app["telegram_bot"].run())


async def cleanup_background_tasks(app):
    logging.info("Removing background tasks")
    app["telegram"].cancel()
    await app["metrics"].result().close()
    await app["telegram"]


def run(telegram_token: str):
    app = web.Application()
    app["telegram_bot"] = Telegram(telegram_token)
    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(cleanup_background_tasks)
    app.add_routes(routes)
    web.run_app(app)
