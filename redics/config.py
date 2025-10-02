from __future__ import annotations

import os
from pathlib import Path
import tomllib
from typing import Self

from pydantic import BaseModel
from yarl import URL


class ConfigError(Exception): ...


class ListLengths(BaseModel):
    name: str
    keys: list[str]


class Config(BaseModel):
    redis_url: str
    list_lengths: ListLengths

    @classmethod
    def from_env(cls) -> Self:
        if not (toml_config_path := (os.environ.get("REDICS_CONFIG"))):
            raise ConfigError("REDICS_CONFIG must be defined")

        with Path(toml_config_path).open("rb") as fp:
            toml = tomllib.load(fp)

        if not (redis_url := os.environ.get("REDICS_REDIS_URL")):
            redis_proto = os.environ.get("REDICS_REDIS_PROTO", "redis")
            redis_host = os.environ.get("REDICS_REDIS_HOST", "127.0.0.1")
            redis_port = os.environ.get("REDICS_REDIS_PORT", "6379")
            redis_db = os.environ.get("REDICS_REDIS_DB", "0")
            redis_url = str(
                URL.build(
                    scheme=redis_proto,
                    host=redis_host,
                    port=int(redis_port),
                    path=redis_db if redis_db.startswith("/") else f"/{redis_db}",
                )
            )

        toml.update({"redis_url": redis_url})
        return cls(**toml)
