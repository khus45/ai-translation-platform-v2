from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Translation Platform"

    APP_ENV: str = "development"

    DEBUG: bool = True

    DATABASE_URL: str

    REDIS_URL: str

    QDRANT_URL: str

    OPENAI_API_KEY: str = ""

    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
