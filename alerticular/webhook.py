import asyncio
import logging
from pprint import pformat

from aiohttp import web
from aiohttp.web_app import Application

import alerticular.target.telegram as telegram
from alerticular.metrics import run_metrics_endpoint

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get("/")
async def handle(request: web.Request) -> web.Response:
    return web.Response(text="Hello World!")


@routes.post("/alertmanager")
async def alertmanager_debug(request: web.Request) -> web.Response:
    message = await request.json()
    logger.info(pformat(message))
    return web.Response(text="Success: Alert logged.")


# This is a placeholder, at a later point these names
# should be provided by the actual available implementations
supported_sources = [
    "alertmanager"
]

# This is a placeholder, at a later point these names
# should be provided by the actual available implementations
supported_targets = [
    "telegram"
]


@routes.post("/from/{source}/to/{chat}/on/{target}")
@routes.post("/from/{source}/to/{target}/{chat}")
@routes.post("/{source}/to/{target}/{chat}")
@routes.post("/{source}/to/{chat}/on/{target}")
@routes.post("/{source}/{target}/{chat}")
async def alertmanager_notify(request: web.Request) -> web.Response:
    source = str(request.match_info.get("source"))
    if source not in supported_sources:
        return web.HTTPBadRequest(
            text=f"Unsupported source {source}. Supported sources: {', '.join(supported_sources)}"
        )

    target = str(request.match_info.get("target"))
    if target not in supported_targets:
        return web.HTTPBadRequest(
            text=f"Unsupported target {target}. Supported targets: {', '.join(supported_targets)}"
        )

    chat = str(request.match_info.get("chat"))

    message = await request.json()
    logger.info(pformat(message))
    if target == "telegram":
        await telegram.send_alert(chat, message)
    return web.Response(text="Success: Alerted {}.".format(chat))


async def on_startup_handler(app: web.Application) -> None:
    logger.info("Adding background tasks")
    app["metrics"] = asyncio.create_task(run_metrics_endpoint())
    app["telegram"] = asyncio.create_task(telegram.run())


async def on_shutdown_handler(app: web.Application) -> None:
    logger.info("Removing background tasks")
    app["telegram"].cancel()
    await app["metrics"].result().close()
    await app["telegram"]


def create_app() -> Application:
    app = web.Application()
    app.on_startup.append(on_startup_handler)
    app.on_shutdown.append(on_shutdown_handler)
    app.add_routes(routes)
    return app


def run(telegram_token: str) -> None:
    telegram.setup(telegram_token)
    app = create_app()
    web.run_app(app)
