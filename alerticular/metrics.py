import logging

from prometheus_async.aio import web as prometheus_async_web
from prometheus_async.aio.web import MetricsHTTPServer

logger = logging.getLogger(__name__)


async def run_metrics_endpoint() -> MetricsHTTPServer:
    logger.info("Starting metrics endpoint")
    return await prometheus_async_web.start_http_server(port=8081)
