from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pathlib import Path


class Settings(BaseSettings):
    APP_ENV: Literal["dev", "prod"] = "dev"
    # API keys
    GEMINI_API_KEY: str
    PERPLEXITY_API_KEY: str
    PERPLEXITY_PROVIDER: str = "perplexity"

    USE_TRACE: bool = True
    USE_MOCK_PERPLEXITY: bool = True
    TRACE_PREVIEW_CHARS: int = 1000
    USE_MOCK_GEMINI: bool = True

    STORAGE_UPLOADS_DIR: str = "storage/uploads"
    STORAGE_OUTPUTS_DIR: str = "storage/outputs"

    MAX_ROWS: int = 1000
    MAX_FILE_MB: int = 10
    REQUEST_TIMEOUT: int = 60
    RETRY_COUNT: int = 3

    TRACE_STORE_FULL_TEXT: bool = False
    TRACE_MAX_CHARS: int = 20000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_TEMPERATURE: float = 0.7

    PERPLEXITY_BASE_URL: str = "https://api.perplexity.ai"
    PERPLEXITY_MODEL: str = "sonar"
    PERPLEXITY_TEMPERATURE: float = 0.2



    @property
    def uploads_path(self) -> Path:
        return Path(self.STORAGE_UPLOADS_DIR)

    @property
    def outputs_path(self) -> Path:
        return Path(self.STORAGE_OUTPUTS_DIR)

    @property
    def is_dev(self) -> bool:
        return self.APP_ENV == "dev"

    @property
    def is_prod(self) -> bool:
        return self.APP_ENV == "prod"

settings = Settings()