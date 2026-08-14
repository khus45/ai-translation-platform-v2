from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

ReviewStatus = Literal["pending", "approved", "rejected", "edited"]


class GlossaryTermCreate(BaseModel):
    term: str = Field(min_length=1, max_length=255)
    approved_translation: str = Field(min_length=1, max_length=255)
    source_language: str = Field(default="en", min_length=2, max_length=20)
    target_language: str = Field(default="hi", min_length=2, max_length=20)
    domain: str = Field(default="general", min_length=2, max_length=50)
    notes: str | None = None

    @field_validator("term", "approved_translation", "domain")
    @classmethod
    def strip_required(cls, value: str) -> str:
        return value.strip()


class GlossaryTermResponse(GlossaryTermCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QAReviewRequest(BaseModel):
    source_text: str = Field(min_length=1, max_length=20_000)
    translated_text: str = Field(min_length=1, max_length=20_000)
    source_language: str | None = Field(default=None, min_length=2, max_length=20)
    target_language: str = Field(min_length=2, max_length=20)
    domain: str | None = Field(default=None, min_length=2, max_length=50)
    translation_id: int | None = None


class QAReportResponse(BaseModel):
    id: int
    translation_id: int | None
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    domain: str
    grammar_score: float
    meaning_score: float
    terminology_score: float
    fluency_score: float
    hallucination_score: float
    overall_score: float
    confidence_score: float
    suggestions: list[str]
    errors: list[str]
    metrics: dict
    retrieved_context: list[dict]
    prompt_version: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=10)
    comment: str = Field(default="", max_length=2000)
    status: ReviewStatus = "pending"
    edited_text: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    translation_id: int
    rating: int
    comment: str
    status: str
    approved: bool | None
    edited_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentIngestRequest(BaseModel):
    filename: str = Field(default="manual-input.txt", min_length=1, max_length=255)
    content_type: str = Field(default="text/plain", max_length=100)
    text: str = Field(min_length=1, max_length=100_000)


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    extracted_text: str
    language: str
    domain: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummaryResponse(BaseModel):
    total_translations: int
    total_reviews: int
    average_quality_score: float
    average_confidence_score: float
    human_approval_rate: float
    provider_usage: dict[str, int]
    language_pairs: dict[str, int]
    top_domains: dict[str, int]
    common_errors: dict[str, int]
    average_latency_ms: float
    estimated_token_cost: float


class TranslationMemoryResponse(BaseModel):
    id: int
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    domain: str
    quality_score: float
    usage_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
