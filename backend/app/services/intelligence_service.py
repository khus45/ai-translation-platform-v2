from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.feedback import Feedback
from app.models.glossary import GlossaryTerm
from app.models.translation_memory import TranslationMemory
from app.models.user import User
from app.repositories.intelligence_repository import (
    AnalyticsRepository,
    DocumentRepository,
    FeedbackRepository,
    GlossaryRepository,
    TranslationMemoryRepository,
)
from app.repositories.translation_repository import TranslationRepository
from app.schemas.intelligence import (
    AnalyticsSummaryResponse,
    DocumentIngestRequest,
    FeedbackCreate,
    GlossaryTermCreate,
)
from app.services.domain_detection import DomainDetectionService
from app.services.language_detection import LanguageDetectionService


class GlossaryService:
    def __init__(self, db: Session):
        self.repository = GlossaryRepository(db)

    def create(
        self, *, request: GlossaryTermCreate, current_user: User
    ) -> GlossaryTerm:
        return self.repository.create(
            user_id=current_user.id,
            term=request.term,
            approved_translation=request.approved_translation,
            source_language=request.source_language,
            target_language=request.target_language,
            domain=request.domain,
            notes=request.notes,
        )

    def list_terms(
        self,
        *,
        current_user: User,
        domain: str | None,
        skip: int,
        limit: int,
    ) -> list[GlossaryTerm]:
        return self.repository.list_for_user(
            user=current_user,
            domain=domain,
            skip=skip,
            limit=limit,
        )


class FeedbackService:
    def __init__(self, db: Session):
        self.repository = FeedbackRepository(db)
        self.translation_repository = TranslationRepository(db)
        self.memory_repository = TranslationMemoryRepository(db)

    def create(
        self,
        *,
        translation_id: int,
        request: FeedbackCreate,
        current_user: User,
    ) -> Feedback:
        translation = self.translation_repository.get_for_user(
            translation_id=translation_id,
            user=current_user,
        )
        if translation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Translation not found",
            )

        approved = self._approved_from_status(request.status)
        feedback = self.repository.create(
            translation_id=translation_id,
            user_id=current_user.id,
            rating=request.rating,
            comment=request.comment,
            status=request.status,
            approved=approved,
            edited_text=request.edited_text,
        )
        if approved or request.status == "edited":
            self.memory_repository.upsert_from_translation(
                user_id=current_user.id,
                source_text=translation.source_text,
                translated_text=request.edited_text or translation.translated_text,
                source_language=translation.source_language,
                target_language=translation.target_language,
                domain=translation.domain,
                quality_score=max(
                    float(request.rating) * 10, translation.confidence_score
                ),
            )
        return feedback

    def _approved_from_status(self, status_value: str) -> bool | None:
        if status_value in {"approved", "edited"}:
            return True
        if status_value == "rejected":
            return False
        return None


class DocumentService:
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.language_detection = LanguageDetectionService()
        self.domain_detection = DomainDetectionService()

    def ingest(self, *, request: DocumentIngestRequest, current_user: User) -> Document:
        language = self.language_detection.detect(request.text).language
        domain = self.domain_detection.detect(request.text).domain
        return self.repository.create(
            user_id=current_user.id,
            filename=request.filename,
            content_type=request.content_type,
            extracted_text=request.text,
            language=language,
            domain=domain,
        )

    def list_documents(
        self,
        *,
        current_user: User,
        skip: int,
        limit: int,
    ) -> list[Document]:
        return self.repository.list_for_user(user=current_user, skip=skip, limit=limit)


class TranslationMemoryService:
    def __init__(self, db: Session):
        self.repository = TranslationMemoryRepository(db)

    def list_memory(
        self,
        *,
        current_user: User,
        skip: int,
        limit: int,
    ) -> list[TranslationMemory]:
        return self.repository.list_for_user(user=current_user, skip=skip, limit=limit)


class AnalyticsService:
    def __init__(self, db: Session):
        self.repository = AnalyticsRepository(db)
        self.feedback_repository = FeedbackRepository(db)

    def summary(self, *, current_user: User) -> AnalyticsSummaryResponse:
        translations = self.repository.translations_for_user(current_user)
        reports = self.repository.reports_for_user(current_user)

        return AnalyticsSummaryResponse(
            total_translations=len(translations),
            total_reviews=len(reports),
            average_quality_score=self._average(
                [report.overall_score for report in reports]
            ),
            average_confidence_score=self._average(
                [translation.confidence_score for translation in translations]
            ),
            human_approval_rate=self.feedback_repository.approval_rate(current_user),
            provider_usage=self._counts(
                [translation.provider for translation in translations]
            ),
            language_pairs=self._counts(
                [
                    f"{translation.source_language}->{translation.target_language}"
                    for translation in translations
                ]
            ),
            top_domains=self._counts(
                [translation.domain for translation in translations]
            ),
            common_errors=self._common_errors(reports),
            average_latency_ms=self._average(
                [float(translation.latency_ms) for translation in translations]
            ),
            estimated_token_cost=round(
                sum(translation.token_cost for translation in translations),
                6,
            ),
        )

    def _average(self, values: list[float]) -> float:
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)

    def _counts(self, values: list[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _common_errors(self, reports) -> dict[str, int]:
        counts: dict[str, int] = {}
        for report in reports:
            for error in report.errors:
                counts[error] = counts.get(error, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10])
