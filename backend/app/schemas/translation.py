from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ProviderName = Literal["auto", "openai", "gemini", "local"]


class TranslationRequest(BaseModel):
    source_text: str = Field(min_length=1, max_length=10_000)
    target_language: str = Field(min_length=2, max_length=20)
    source_language: str | None = Field(default=None, min_length=2, max_length=20)
    provider: ProviderName = "auto"

    @field_validator("source_text", "target_language", "source_language")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()


class TranslationResponse(BaseModel):
    id: int
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    translation_model: str
    confidence_score: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LanguageDetectionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class LanguageDetectionResponse(BaseModel):
    language: str
    confidence_score: float


class TranslationErrorResponse(BaseModel):
    detail: str
    attempted_providers: list[str] = []
