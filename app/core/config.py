"""
Central Configuration Module.

This module defines the application settings using Pydantic BaseSettings.
Settings are resolved in this priority order:
    1. Environment variables (e.g. PORT=3000 python main.py)
    2. .env.<ENV> file       (e.g. .env.dev, .env.stage, .env.prod)
    3. Default values below
"""

import os
from importlib.metadata import metadata
from typing import ClassVar, Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.lib import decode_meta

# Read meta from .toml file as single source
_meta = metadata("flow-builder-backend")


class _Settings(BaseSettings):
    APP_NAME: str = _meta["Name"].replace("-", " ").title()
    APP_VERSION: str = _meta["Version"]
    APP_DESCRIPTION: str = decode_meta(_meta["Summary"])

    # ----------------------------------------------------------------
    # ⚙️  Environment — resolved at class-definition time so that
    #     ENV_FILE is available before Pydantic starts loading fields.
    # ----------------------------------------------------------------
    ENV: ClassVar[str] = os.getenv("ENV", "dev")
    ENV_FILE: ClassVar[str] = f".env.{ENV}"  # e.g. .env.dev

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,  # HOST == host == Host in env vars
        extra="ignore",  # silently drop unknown env vars
    )

    # ----------------------------------------------------------------
    # 📂  Server
    # ----------------------------------------------------------------
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = False  # always opt-in to debug; never default True

    # ----------------------------------------------------------------
    # 📝  Logging
    # ----------------------------------------------------------------
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: str = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )

    # ----------------------------------------------------------------
    # Validators
    # ----------------------------------------------------------------
    @field_validator("PORT")
    @classmethod
    def port_must_be_valid(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError(f"PORT must be between 1 and 65535, got {v}")
        return v


# Singleton — import this everywhere, never instantiate _Settings directly
settings = _Settings()
