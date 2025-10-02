from __future__ import annotations

import asyncio
from dataclasses import dataclass
import datetime
from typing import Awaitable

from falcon.asgi import Request, Response
from redis.asyncio import Redis

from .config import ListLengths
from .decorator import log_error


@dataclass
class Metrics:
    list_lengths: ListLengths

    @log_error
    async def on_get(self, req: Request, resp: Response) -> None:
        redis: Redis = req.scope["state"]["redis"]
        timestamp = millis_since_epoch()

        list_lengths = await asyncio.gather(
            *(
                # the redis library doesn't properly type itself - this is typed as if
                # it might return int (not Awaitable[int]) despite being an async Redis
                with_key(key, redis.llen(key))  # type: ignore[bad-argument-type]
                for key in self.list_lengths.keys
            )
        )

        redis_list_length = [
            f"# HELP {self.list_lengths.name} Length of redis lists.",
            f"# TYPE {self.list_lengths.name} gauge",
        ]
        redis_list_length.extend(
            f"""{self.list_lengths.name}{{list="{key}"}} {value} {timestamp}"""
            for key, value in list_lengths
        )

        resp.content_type = "text/plain; version=0.0.4"
        resp.text = "\n".join(redis_list_length)


def millis_since_epoch() -> int:
    now = datetime.datetime.now(tz=datetime.UTC)
    return int(now.timestamp() * 1000)


async def with_key[T](key: str, awaitable: Awaitable[T]) -> tuple[str, T]:
    return key, await awaitable
