import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Union

from fastapi.logger import logger as fast_api_logger
from pydantic import PostgresDsn, TypeAdapter
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int
    DB_SCHEMA: str
    API_PREFIX: str = "/api/v1"
    APP_NAME: str = "Airport MAnager API"
    VERSION: str = "0.0.1"
    DOCS_PATH: str = "docs"
    OPENAPI_PATH: str = "openapi.json"
    JWT_SECRET_KEY: str = "TOP_SECRET_JWT"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 120 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    JWT_REFRESH_SECRET_KEY: str = "JWT_REFRESH_SECRET_KEY"
    STAGE: str = "DEVELOPMENT"
    ALLOW_ORIGINS: List = ["*"]
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ROOT_DIR: Path = Path("/data")
    BROKER_URI: str = "amqp://rabbitmq_server:5672"
    BACKEND_URI: str = "redis://redis_server:6379/0"
    LOGGER_LEVEL: int = logging.INFO
    FORMAT: str = "APP_%(levelname)s: %(asctime)s [%(pathname)s:%(lineno)d] %(message)s"
    DATEFMT: str = "%d-%m-%Y %I:%M:%S"

    @property
    def ADD_DEV_ROUTERS(self) -> bool:
        return self.STAGE == "DEVELOPMENT"

    @property
    def SQLALCHAMY_DATABASE_URL(self) -> PostgresDsn:
        url = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}"
        dsn = f"{self.DB_SCHEMA}://{url}/{self.POSTGRES_DB}"
        return TypeAdapter(PostgresDsn).validate_python(dsn)

    @property
    def DOCS_URL(self) -> Union[str, None]:
        return f"{self.API_PREFIX}/{self.DOCS_PATH}"

    @property
    def OPENAPI_URL(self) -> str:
        return f"{self.API_PREFIX}/{self.OPENAPI_PATH}"

    class Config:
        env_file = ".env"
        case_sensitive = True


class Dev(CommonSettings):
    ...


class Prod(CommonSettings):
    ALLOW_ORIGINS: List[str] = [""]

    @property
    def DOCS_URL(self) -> None:
        return None

    @property
    def OPENAPI_URL(self) -> None:
        return None


@lru_cache()
def get_settings() -> Union[Dev, Prod]:
    map_config = dict(production=Prod, development=Dev)
    get_env_stage = os.environ.get("STAGE", "DEVELOPMENT").lower()
    config_env = map_config.get(get_env_stage, Dev)
    return config_env()  # type: ignore


def add_relative_path(record):
    record["extra"]["relative_path"] = record["name"].replace(".", "/") + ".py"


@lru_cache()
def get_logger():
    settings = get_settings()
    logging.basicConfig(
        level=settings.LOGGER_LEVEL, format=settings.FORMAT, datefmt=settings.DATEFMT
    )
    gunicorn_logger = logging.getLogger("gunicorn.error")
    fast_api_logger.handlers = gunicorn_logger.handlers
    fast_api_logger.setLevel(gunicorn_logger.level)
    return fast_api_logger


settings = get_settings()
app_logger = get_logger()
