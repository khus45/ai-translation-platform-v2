from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class GlossaryTerm(BaseModel):
    __tablename__ = "glossary_terms"

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    term: Mapped[str] = mapped_column(String(255), index=True)
    approved_translation: Mapped[str] = mapped_column(String(255))
    source_language: Mapped[str] = mapped_column(String(20), default="en")
    target_language: Mapped[str] = mapped_column(String(20), default="hi")
    domain: Mapped[str] = mapped_column(String(50), default="general", index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
