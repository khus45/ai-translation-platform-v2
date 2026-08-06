from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from tenacity import RetryError, Retrying, stop_after_attempt, wait_exponential

from app.config.settings import settings
from app.models.translation import Translation
from app.models.user import User
from app.repositories.translation_repository import TranslationRepository
from app.schemas.translation import TranslationRequest
from app.services.ai.base_provider import (
    AIProviderError,
    AIProviderUnavailableError,
    BaseTranslationProvider,
    TranslationResult,
)
from app.services.ai.provider_factory import ProviderFactory
from app.services.language_detection import LanguageDetectionService
from app.services.prompt_builder import PromptBuilder


class TranslationService:
    def __init__(self, db: Session):
        prompt_builder = PromptBuilder()
        self.repository = TranslationRepository(db)
        self.language_detection = LanguageDetectionService()
        self.provider_factory = ProviderFactory(prompt_builder)

    def translate(
        self,
        *,
        request: TranslationRequest,
        current_user: User,
    ) -> Translation:
        source_language = request.source_language
        if not source_language or source_language.lower() == "auto":
            source_language = self.language_detection.detect(
                request.source_text
            ).language

        result = self._translate_with_fallbacks(
            request=request,
            source_language=source_language,
        )
        return self.repository.create(
            user_id=current_user.id,
            source_text=request.source_text,
            result=result,
        )

    def detect_language(self, text: str):
        return self.language_detection.detect(text)

    def list_translations(
        self,
        *,
        current_user: User,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Translation]:
        return self.repository.list_for_user(user=current_user, skip=skip, limit=limit)

    def get_translation(
        self, *, translation_id: int, current_user: User
    ) -> Translation:
        translation = self.repository.get_for_user(
            translation_id=translation_id,
            user=current_user,
        )
        if translation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Translation not found",
            )
        return translation

    def delete_translation(self, *, translation_id: int, current_user: User) -> None:
        translation = self.get_translation(
            translation_id=translation_id,
            current_user=current_user,
        )
        self.repository.delete(translation)

    def _translate_with_fallbacks(
        self,
        *,
        request: TranslationRequest,
        source_language: str,
    ) -> TranslationResult:
        provider_names = self.provider_factory.provider_sequence(request.provider)
        errors: list[str] = []

        for provider_name in provider_names:
            try:
                provider = self.provider_factory.create(provider_name)
                return self._translate_with_retries(
                    provider=provider,
                    request=request,
                    source_language=source_language,
                )
            except (
                AIProviderError,
                AIProviderUnavailableError,
                RetryError,
                ValueError,
            ) as exc:
                errors.append(f"{provider_name}: {exc}")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": "All translation providers failed",
                "attempted_providers": provider_names,
                "errors": errors,
            },
        )

    def _translate_with_retries(
        self,
        *,
        provider: BaseTranslationProvider,
        request: TranslationRequest,
        source_language: str,
    ) -> TranslationResult:
        retryer = Retrying(
            stop=stop_after_attempt(settings.TRANSLATION_MAX_RETRIES + 1),
            wait=wait_exponential(multiplier=0.2, min=0.2, max=1),
            reraise=True,
        )
        for attempt in retryer:
            with attempt:
                return provider.translate(
                    source_text=request.source_text,
                    source_language=source_language,
                    target_language=request.target_language,
                )
        raise AIProviderError("Translation retry loop exited unexpectedly")
