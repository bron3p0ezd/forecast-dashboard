import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


def _get_env_path() -> str:
    env_path = os.path.join(BASE_DIR, "envs", ".env")
    return env_path


class Settings(BaseSettings):
    DB_PATH: Path

    DOCS_URL_ENABLED: Optional[str] = None
    REDOC_URL_ENABLED: Optional[str] = None
    OPENAPI_URL_ENABLED: Optional[str] = None

    ALLOW_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    model_config = SettingsConfigDict(env_file=_get_env_path())


settings = Settings()  # type: ignore
