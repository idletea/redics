from __future__ import annotations

from functools import wraps
from typing import Awaitable, Callable, ParamSpec

import structlog

log = structlog.get_logger()

P = ParamSpec("P")


def log_error[T, **P](fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(fn)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await fn(*args, **kwargs)
        except Exception:
            log.exception()
            raise

    return inner
