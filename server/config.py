"""Application configuration."""

import logging
from functools import lru_cache

from fastapi.logger import logger as fastapi_logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    debug: bool = False
    database_name: str = "fastapi-app"
    database_username: str = "postgres"
    database_password: str = "postgres"
    database_host: str = "db"
    database_port: int = 5432
    cache_host: str = "redis"
    cache_port: int = 6379
    cache_db: int = 0
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.database_username}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def database_url_sync(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.database_username}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.cache_host}:{self.cache_port}/{self.cache_db}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


def configure_logging(level: str) -> None:
    """Configure app logging once."""

    logging.basicConfig(level=level, format="%(levelname)s: %(name)s: %(message)s")
    fastapi_logger.setLevel(level)


settings = get_settings()
