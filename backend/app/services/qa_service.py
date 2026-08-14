from sqlalchemy.orm import Session

from app.models.quality_report import QualityReport
from app.models.user import User
from app.repositories.intelligence_repository import QualityReportRepository
from app.schemas.intelligence import QAReviewRequest
from app.services.domain_detection import DomainDetectionService
from app.services.evaluation_service import EvaluationService
from app.services.language_detection import LanguageDetectionService
from app.services.qa_agents import (
    GrammarAgent,
    HallucinationAgent,
    ReviewerAgent,
    TerminologyAgent,
)
from app.services.rag_service import RAGService


class QAService:
    def __init__(self, db: Session):
        self.repository = QualityReportRepository(db)
        self.language_detection = LanguageDetectionService()
        self.domain_detection = DomainDetectionService()
        self.rag = RAGService(db)
        self.evaluation = EvaluationService()
        self.grammar_agent = GrammarAgent()
        self.terminology_agent = TerminologyAgent()
        self.hallucination_agent = HallucinationAgent()
        self.reviewer_agent = ReviewerAgent()

    def review(self, *, request: QAReviewRequest, current_user: User) -> QualityReport:
        source_language = (
            request.source_language
            or self.language_detection.detect(request.source_text).language
        )
        domain = (
            request.domain or self.domain_detection.detect(request.source_text).domain
        )
        context = self.rag.retrieve_context(
            user=current_user,
            source_text=request.source_text,
            source_language=source_language,
            target_language=request.target_language,
            domain=domain,
        )
        missing_terms = self.rag.glossary_term_gaps(
            source_text=request.source_text,
            translated_text=request.translated_text,
            context=context,
        )
        metrics = self.evaluation.evaluate(
            source_text=request.source_text,
            translated_text=request.translated_text,
            glossary_hits=sum(1 for item in context if item.get("type") == "glossary"),
            missing_terms=len(missing_terms),
        )
        grammar = self.grammar_agent.review(request.translated_text)
        terminology = self.terminology_agent.review(missing_terms)
        hallucination = self.hallucination_agent.review(
            request.source_text,
            request.translated_text,
        )
        summary = self.reviewer_agent.summarize(
            grammar=grammar,
            terminology=terminology,
            hallucination=hallucination,
            metrics=metrics,
        )
        errors = [*grammar.errors, *terminology.errors, *hallucination.errors]
        suggestions = [
            *grammar.suggestions,
            *terminology.suggestions,
            *hallucination.suggestions,
        ]

        return self.repository.create(
            translation_id=request.translation_id,
            user_id=current_user.id,
            source_text=request.source_text,
            translated_text=request.translated_text,
            source_language=source_language,
            target_language=request.target_language,
            domain=domain,
            suggestions=suggestions,
            errors=errors,
            metrics=metrics,
            retrieved_context=context,
            prompt_version="qa-v1",
            **summary,
        )

    def list_reports(
        self,
        *,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> list[QualityReport]:
        return self.repository.list_for_user(user=current_user, skip=skip, limit=limit)
