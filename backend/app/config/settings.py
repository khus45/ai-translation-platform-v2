from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Translation Platform"
    DATABASE_URL: str
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Translation Platform"
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    DEFAULT_TRANSLATION_PROVIDER: str = "openai"
    OPENAI_TRANSLATION_MODEL: str = "gpt-4o-mini"
    GEMINI_TRANSLATION_MODEL: str = "gemini-1.5-flash"
    TRANSLATION_MAX_RETRIES: int = Field(default=2, ge=0, le=5)
    CORS_ALLOW_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
