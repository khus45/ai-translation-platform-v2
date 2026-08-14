from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.intelligence import (
    AnalyticsSummaryResponse,
    DocumentIngestRequest,
    DocumentResponse,
    FeedbackCreate,
    FeedbackResponse,
    GlossaryTermCreate,
    GlossaryTermResponse,
    QAReportResponse,
    QAReviewRequest,
    TranslationMemoryResponse,
)
from app.services.intelligence_service import (
    AnalyticsService,
    DocumentService,
    FeedbackService,
    GlossaryService,
    TranslationMemoryService,
)
from app.services.qa_service import QAService

router = APIRouter(tags=["AI Intelligence"])


@router.post(
    "/qa/review",
    response_model=QAReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def review_translation_quality(
    request: QAReviewRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return QAService(db).review(request=request, current_user=current_user)


@router.get("/qa/reports", response_model=list[QAReportResponse])
def list_quality_reports(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return QAService(db).list_reports(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/glossary",
    response_model=GlossaryTermResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_glossary_term(
    request: GlossaryTermCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return GlossaryService(db).create(request=request, current_user=current_user)


@router.get("/glossary", response_model=list[GlossaryTermResponse])
def list_glossary_terms(
    domain: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return GlossaryService(db).list_terms(
        current_user=current_user,
        domain=domain,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/translations/{translation_id}/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    translation_id: int,
    request: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return FeedbackService(db).create(
        translation_id=translation_id,
        request=request,
        current_user=current_user,
    )


@router.get("/translation-memory", response_model=list[TranslationMemoryResponse])
def list_translation_memory(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return TranslationMemoryService(db).list_memory(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/documents/ingest",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_document(
    request: DocumentIngestRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return DocumentService(db).ingest(request=request, current_user=current_user)


@router.get("/documents", response_model=list[DocumentResponse])
def list_documents(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return DocumentService(db).list_documents(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
def analytics_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return AnalyticsService(db).summary(current_user=current_user)
