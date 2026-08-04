from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Feedback(BaseModel):
    __tablename__ = "feedback"

    translation_id: Mapped[int] = mapped_column(ForeignKey("translations.id"))

    rating: Mapped[int] = mapped_column(Integer)

    comment: Mapped[str] = mapped_column(Text)
