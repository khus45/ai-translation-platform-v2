from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class QualityReport(BaseModel):
    __tablename__ = "quality_reports"

    translation_id: Mapped[int | None] = mapped_column(
        ForeignKey("translations.id"),
        nullable=True,
        index=True,
    )
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    source_text: Mapped[str] = mapped_column(Text)
    translated_text: Mapped[str] = mapped_column(Text)
    source_language: Mapped[str] = mapped_column(String(20))
    target_language: Mapped[str] = mapped_column(String(20))
    domain: Mapped[str] = mapped_column(String(50), default="general")
    grammar_score: Mapped[float] = mapped_column(Float)
    meaning_score: Mapped[float] = mapped_column(Float)
    terminology_score: Mapped[float] = mapped_column(Float)
    fluency_score: Mapped[float] = mapped_column(Float)
    hallucination_score: Mapped[float] = mapped_column(Float)
    overall_score: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float)
    suggestions: Mapped[list[str]] = mapped_column(JSON, default=list)
    errors: Mapped[list[str]] = mapped_column(JSON, default=list)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    retrieved_context: Mapped[list[dict]] = mapped_column(JSON, default=list)
    prompt_version: Mapped[str] = mapped_column(String(50), default="qa-v1")
