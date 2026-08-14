from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.feedback import Feedback
from app.models.glossary import GlossaryTerm
from app.models.quality_report import QualityReport
from app.models.translation import Translation
from app.models.translation_memory import TranslationMemory
from app.models.user import User


class GlossaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        term: str,
        approved_translation: str,
        source_language: str,
        target_language: str,
        domain: str,
        notes: str | None,
    ) -> GlossaryTerm:
        glossary_term = GlossaryTerm(
            user_id=user_id,
            term=term,
            approved_translation=approved_translation,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            notes=notes,
        )
        self.db.add(glossary_term)
        self.db.commit()
        self.db.refresh(glossary_term)
        return glossary_term

    def list_for_user(
        self,
        *,
        user: User,
        domain: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[GlossaryTerm]:
        statement = select(GlossaryTerm).order_by(GlossaryTerm.term)
        if user.role != "admin":
            statement = statement.where(GlossaryTerm.user_id == user.id)
        if domain:
            statement = statement.where(GlossaryTerm.domain == domain)
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())

    def search_relevant(
        self,
        *,
        user_id: int,
        text: str,
        source_language: str,
        target_language: str,
        domain: str,
        limit: int = 8,
    ) -> list[GlossaryTerm]:
        terms = self.db.scalars(
            select(GlossaryTerm).where(
                GlossaryTerm.user_id == user_id,
                GlossaryTerm.source_language == source_language,
                GlossaryTerm.target_language == target_language,
            )
        ).all()
        lowered = text.lower()
        relevant = [
            term
            for term in terms
            if term.term.lower() in lowered
            or term.domain == domain
            or term.domain == "general"
        ]
        return relevant[:limit]


class QualityReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **values) -> QualityReport:
        report = QualityReport(**values)
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_for_user(
        self,
        *,
        user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> list[QualityReport]:
        statement = select(QualityReport).order_by(QualityReport.created_at.desc())
        if user.role != "admin":
            statement = statement.where(QualityReport.user_id == user.id)
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **values) -> Feedback:
        feedback = Feedback(**values)
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def approval_rate(self, user: User) -> float:
        statement = select(Feedback)
        if user.role != "admin":
            statement = statement.where(Feedback.user_id == user.id)
        feedback_items = list(self.db.scalars(statement).all())
        reviewed = [item for item in feedback_items if item.approved is not None]
        if not reviewed:
            return 0.0
        approved = sum(1 for item in reviewed if item.approved)
        return round(approved / len(reviewed), 4)


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **values) -> Document:
        document = Document(**values)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def list_for_user(self, *, user: User, skip: int, limit: int) -> list[Document]:
        statement = select(Document).order_by(Document.created_at.desc())
        if user.role != "admin":
            statement = statement.where(Document.user_id == user.id)
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())


class TranslationMemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_from_translation(
        self,
        *,
        user_id: int,
        source_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        domain: str,
        quality_score: float,
    ) -> TranslationMemory:
        existing = self.db.scalar(
            select(TranslationMemory).where(
                TranslationMemory.user_id == user_id,
                func.lower(TranslationMemory.source_text) == source_text.lower(),
                TranslationMemory.source_language == source_language,
                TranslationMemory.target_language == target_language,
            )
        )
        if existing:
            existing.translated_text = translated_text
            existing.domain = domain
            existing.quality_score = max(existing.quality_score, quality_score)
            existing.usage_count += 1
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            return existing

        memory = TranslationMemory(
            user_id=user_id,
            source_text=source_text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            quality_score=quality_score,
        )
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def find_exact(
        self,
        *,
        user_id: int,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationMemory | None:
        return self.db.scalar(
            select(TranslationMemory).where(
                TranslationMemory.user_id == user_id,
                func.lower(TranslationMemory.source_text) == source_text.lower(),
                TranslationMemory.source_language == source_language,
                TranslationMemory.target_language == target_language,
            )
        )

    def mark_used(self, memory: TranslationMemory) -> TranslationMemory:
        memory.usage_count += 1
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory

    def list_for_user(
        self,
        *,
        user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TranslationMemory]:
        statement = select(TranslationMemory).order_by(
            TranslationMemory.usage_count.desc(),
            TranslationMemory.updated_at.desc(),
        )
        if user.role != "admin":
            statement = statement.where(TranslationMemory.user_id == user.id)
        return list(self.db.scalars(statement.offset(skip).limit(limit)).all())

    def search_similar(
        self,
        *,
        user_id: int,
        source_text: str,
        source_language: str,
        target_language: str,
        limit: int = 5,
    ) -> list[TranslationMemory]:
        memories = self.db.scalars(
            select(TranslationMemory).where(
                TranslationMemory.user_id == user_id,
                TranslationMemory.source_language == source_language,
                TranslationMemory.target_language == target_language,
            )
        ).all()
        source_words = set(source_text.lower().split())
        scored = []
        for memory in memories:
            memory_words = set(memory.source_text.lower().split())
            overlap = len(source_words & memory_words)
            if overlap:
                scored.append((overlap, memory))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [memory for _, memory in scored[:limit]]


class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def translations_for_user(self, user: User) -> list[Translation]:
        statement = select(Translation)
        if user.role != "admin":
            statement = statement.where(Translation.user_id == user.id)
        return list(self.db.scalars(statement).all())

    def reports_for_user(self, user: User) -> list[QualityReport]:
        statement = select(QualityReport)
        if user.role != "admin":
            statement = statement.where(QualityReport.user_id == user.id)
        return list(self.db.scalars(statement).all())
