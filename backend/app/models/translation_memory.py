from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class TranslationMemory(BaseModel):
    __tablename__ = "translation_memory"

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    source_text: Mapped[str] = mapped_column(Text)
    translated_text: Mapped[str] = mapped_column(Text)
    source_language: Mapped[str] = mapped_column(String(20))
    target_language: Mapped[str] = mapped_column(String(20))
    domain: Mapped[str] = mapped_column(String(50), default="general", index=True)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    usage_count: Mapped[int] = mapped_column(Integer, default=1)
