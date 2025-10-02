from __future__ import annotations

import asyncio
from typing import Any, Mapping

import redis.asyncio as redis
import structlog

log = structlog.get_logger()


class RedisConnector:
    """Middleware to inject a shared redis connection across all requests.

    https://asgi.readthedocs.io/en/latest/specs/lifespan.html
    """

    redis_url: str

    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url

    async def process_startup(
        self,
        scope: Mapping[str, Any],
        event: Mapping[str, Any],  # noqa: ARG002
    ) -> None:
        # https://asgi.readthedocs.io/en/latest/specs/lifespan.html#lifespan-state
        if "state" not in scope:
            error = "redics requires the ASGI server implement the state feature"
            log.error(error)
            raise RuntimeError(error)

        redis_connection = redis.from_url(self.redis_url)
        try:
            async with asyncio.timeout(5):
                await redis_connection.ping()
        except asyncio.TimeoutError:
            log.exception("failed to connect to redis")
            raise
        else:
            log.info("connected to redis")

        scope["state"]["redis"] = redis_connection

    async def process_shutdown(
        self,
        scope: Mapping[str, Any],
        event: Mapping[str, Any],  # noqa: ARG002
    ) -> None:
        redis_connection: redis.Redis = scope["state"]["redis"]
        del scope["state"]["redis"]

        await redis_connection.aclose()
        log.info("disconnected from redis")
