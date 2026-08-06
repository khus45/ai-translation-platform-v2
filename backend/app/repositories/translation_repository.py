from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.translation import Translation
from app.models.user import User
from app.services.ai.base_provider import TranslationResult


class TranslationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        source_text: str,
        result: TranslationResult,
    ) -> Translation:
        translation = Translation(
            user_id=user_id,
            source_text=source_text,
            translated_text=result.translated_text,
            source_language=result.source_language,
            target_language=result.target_language,
            translation_model=result.translation_model,
            provider=result.provider,
            confidence_score=result.confidence_score,
        )
        self.db.add(translation)
        self.db.commit()
        self.db.refresh(translation)
        return translation

    def list_for_user(
        self,
        *,
        user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Translation]:
        statement = select(Translation).order_by(Translation.created_at.desc())
        if user.role != "admin":
            statement = statement.where(Translation.user_id == user.id)
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())

    def get_for_user(self, *, translation_id: int, user: User) -> Translation | None:
        statement = select(Translation).where(Translation.id == translation_id)
        if user.role != "admin":
            statement = statement.where(Translation.user_id == user.id)
        return self.db.scalar(statement)

    def delete(self, translation: Translation) -> None:
        self.db.delete(translation)
        self.db.commit()
