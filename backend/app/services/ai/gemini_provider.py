from app.config.settings import settings
from app.services.ai.base_provider import (
    AIProviderError,
    AIProviderUnavailableError,
    BaseTranslationProvider,
    TranslationResult,
)
from app.services.prompt_builder import PromptBuilder


class GeminiTranslationProvider(BaseTranslationProvider):
    provider_name = "gemini"

    def __init__(self, prompt_builder: PromptBuilder | None = None):
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.model = settings.GEMINI_TRANSLATION_MODEL

    def translate(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationResult:
        api_key = self._valid_api_key(settings.GEMINI_API_KEY)
        if not api_key:
            raise AIProviderUnavailableError("Gemini API key is not configured")

        prompt = self.prompt_builder.build_translation_prompt(
            source_text=source_text,
            source_language=source_language,
            target_language=target_language,
        )

        try:
            translated_text = self._generate_with_google_genai(api_key, prompt)
        except AIProviderUnavailableError:
            raise
        except Exception as exc:
            raise AIProviderError(f"Gemini translation failed: {exc}") from exc

        if not translated_text:
            raise AIProviderError("Gemini returned an empty translation")

        return TranslationResult(
            translated_text=translated_text.strip(),
            source_language=source_language,
            target_language=target_language,
            provider=self.provider_name,
            translation_model=self.model,
            confidence_score=0.88,
        )

    def _generate_with_google_genai(self, api_key: str, prompt: str) -> str:
        try:
            from google import genai
        except ImportError as exc:
            raise AIProviderUnavailableError(
                "google-genai package is not installed"
            ) from exc

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return getattr(response, "text", "") or ""

    def _valid_api_key(self, api_key: str | None) -> str | None:
        if not api_key or api_key.startswith("your_"):
            return None
        return api_key
