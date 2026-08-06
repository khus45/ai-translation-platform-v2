from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Translation(BaseModel):
    __tablename__ = "translations"

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    source_text: Mapped[str] = mapped_column(Text)

    translated_text: Mapped[str] = mapped_column(Text)

    source_language: Mapped[str] = mapped_column(String(20))

    target_language: Mapped[str] = mapped_column(String(20))

    translation_model: Mapped[str] = mapped_column(String(100))

    provider: Mapped[str] = mapped_column(String(50), default="local")

    confidence_score: Mapped[float] = mapped_column(Float)
