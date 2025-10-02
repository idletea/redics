from __future__ import annotations

import os
from pathlib import Path
import tomllib
from typing import Self

from pydantic import BaseModel


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

        if redis_url := os.environ.get("REDICS_REDIS_URL"):
            toml.update({"redis_url": redis_url})

        return cls(**toml)
