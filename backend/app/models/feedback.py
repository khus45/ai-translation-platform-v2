from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Feedback(BaseModel):
    __tablename__ = "feedback"

    translation_id: Mapped[int] = mapped_column(ForeignKey("translations.id"))

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)

    rating: Mapped[int] = mapped_column(Integer)

    comment: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(30), default="pending")

    approved: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    edited_text: Mapped[str | None] = mapped_column(Text, nullable=True)
