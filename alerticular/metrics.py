import logging
from prometheus_client import Histogram
from prometheus_async.aio import time
from prometheus_async.aio import web as prometheus_async_web

logger = logging.getLogger(__name__)


async def run_metrics_endpoint():
    logger.info("Starting metrics endpoint")
    return await prometheus_async_web.start_http_server(port=8081)
