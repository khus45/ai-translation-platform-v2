from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Translation(BaseModel):
    __tablename__ = "translations"

    source_text: Mapped[str] = mapped_column(Text)

    translated_text: Mapped[str] = mapped_column(Text)

    source_language: Mapped[str] = mapped_column(String(20))

    target_language: Mapped[str] = mapped_column(String(20))

    translation_model: Mapped[str] = mapped_column(String(100))

    confidence_score: Mapped[float] = mapped_column(Float)
