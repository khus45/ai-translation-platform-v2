from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.translation import Translation
from app.models.user import User
from app.schemas.translation import (
    LanguageDetectionRequest,
    LanguageDetectionResponse,
    TranslationRequest,
    TranslationResponse,
)
from app.services.translation_service import TranslationService

router = APIRouter(tags=["Translations"])


@router.post("/translate", response_model=TranslationResponse)
def translate_text(
    request: TranslationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Translation:
    return TranslationService(db).translate(
        request=request,
        current_user=current_user,
    )


@router.post("/detect-language", response_model=LanguageDetectionResponse)
def detect_language(
    request: LanguageDetectionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return TranslationService(db).detect_language(request.text)


@router.get("/translations", response_model=list[TranslationResponse])
def list_translations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> list[Translation]:
    return TranslationService(db).list_translations(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )


@router.get("/translations/{translation_id}", response_model=TranslationResponse)
def get_translation(
    translation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Translation:
    return TranslationService(db).get_translation(
        translation_id=translation_id,
        current_user=current_user,
    )


@router.delete("/translations/{translation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_translation(
    translation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Response:
    TranslationService(db).delete_translation(
        translation_id=translation_id,
        current_user=current_user,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
