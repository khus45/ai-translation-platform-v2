from abc import ABC, abstractmethod
from dataclasses import dataclass


class AIProviderError(Exception):
    pass


class AIProviderUnavailableError(AIProviderError):
    pass


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    translation_model: str
    confidence_score: float


class BaseTranslationProvider(ABC):
    provider_name: str

    @abstractmethod
    def translate(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationResult:
        raise NotImplementedError
