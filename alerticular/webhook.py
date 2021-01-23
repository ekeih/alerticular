import asyncio
from aiohttp import web
import logging
from pprint import pformat
import alerticular.telegram as telegram
from alerticular.metrics import run_metrics_endpoint

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get("/")
async def handle(request):
    return web.Response(text="Hello World!")


@routes.get("/telegram/{chat}/spam")
async def spam(request):
    chat = request.match_info.get("chat")
    await telegram.bot.send_message(chat, "Spam, Spam, Spam!")
    return web.Response(text="Success: {} got spammed.".format(chat))


@routes.post("/alertmanager")
async def alertmanager_debug(request):
    message = await request.json()
    logger.info(pformat(message))
    return web.Response(text="Success: Alert logged.")


@routes.post("/alertmanager/{chat}")
async def alertmanager_notify(request):
    chat = request.match_info.get("chat")
    message = await request.json()
    logger.info(pformat(message))
    await telegram.send_alert(chat, message)
    return web.Response(text="Success: Alerted {}.".format(chat))


async def start_background_tasks(app):
    logger.info("Adding background tasks")
    app["metrics"] = asyncio.create_task(run_metrics_endpoint())
    app["telegram"] = asyncio.create_task(telegram.run())


async def cleanup_background_tasks(app):
    logger.info("Removing background tasks")
    app["telegram"].cancel()
    await app["metrics"].result().close()
    await app["telegram"]


def run(telegram_token: str):
    app = web.Application()
    telegram.setup(telegram_token)
    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(cleanup_background_tasks)
    app.add_routes(routes)
    web.run_app(app)
