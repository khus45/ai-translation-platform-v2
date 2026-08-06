from app.config.settings import settings
from app.services.ai.base_provider import BaseTranslationProvider
from app.services.ai.gemini_provider import GeminiTranslationProvider
from app.services.ai.local_provider import LocalFallbackProvider
from app.services.ai.openai_provider import OpenAITranslationProvider
from app.services.prompt_builder import PromptBuilder


class ProviderFactory:
    def __init__(self, prompt_builder: PromptBuilder | None = None):
        self.prompt_builder = prompt_builder or PromptBuilder()

    def create(self, provider_name: str) -> BaseTranslationProvider:
        provider = provider_name.strip().lower()
        if provider == "openai":
            return OpenAITranslationProvider(self.prompt_builder)
        if provider == "gemini":
            return GeminiTranslationProvider(self.prompt_builder)
        if provider == "local":
            return LocalFallbackProvider(self.prompt_builder)
        raise ValueError(f"Unsupported translation provider: {provider_name}")

    def provider_sequence(self, requested_provider: str | None) -> list[str]:
        provider = (requested_provider or "auto").strip().lower()
        if provider != "auto":
            return self._with_local_fallback([provider])

        preferred = settings.DEFAULT_TRANSLATION_PROVIDER.strip().lower()
        return self._with_local_fallback([preferred, "openai", "gemini"])

    def _with_local_fallback(self, providers: list[str]) -> list[str]:
        sequence: list[str] = []
        for provider in [*providers, "local"]:
            if provider not in sequence:
                sequence.append(provider)
        return sequence
