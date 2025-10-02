from __future__ import annotations

import falcon
import falcon.asgi
import structlog

from .config import Config
from .metrics import Metrics
from .redis import RedisConnector

log = structlog.get_logger()
config = Config.from_env()

app = falcon.asgi.App(middleware=[RedisConnector(redis_url=config.redis_url)])
app.add_route("/metrics", Metrics(list_lengths=config.list_lengths))
