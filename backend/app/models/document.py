from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Document(BaseModel):
    __tablename__ = "documents"

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100), default="text/plain")
    extracted_text: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(20), default="unknown")
    domain: Mapped[str] = mapped_column(String(50), default="general")
