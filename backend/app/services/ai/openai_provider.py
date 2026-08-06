from app.config.settings import settings
from app.services.ai.base_provider import (
    AIProviderError,
    AIProviderUnavailableError,
    BaseTranslationProvider,
    TranslationResult,
)
from app.services.prompt_builder import PromptBuilder


class OpenAITranslationProvider(BaseTranslationProvider):
    provider_name = "openai"

    def __init__(self, prompt_builder: PromptBuilder | None = None):
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.model = settings.OPENAI_TRANSLATION_MODEL

    def translate(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationResult:
        api_key = self._valid_api_key(settings.OPENAI_API_KEY)
        if not api_key:
            raise AIProviderUnavailableError("OpenAI API key is not configured")

        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model=self.model,
                messages=self.prompt_builder.build_openai_messages(
                    source_text=source_text,
                    source_language=source_language,
                    target_language=target_language,
                ),
                temperature=0.2,
            )
            translated_text = completion.choices[0].message.content
        except Exception as exc:
            raise AIProviderError(f"OpenAI translation failed: {exc}") from exc

        if not translated_text:
            raise AIProviderError("OpenAI returned an empty translation")

        return TranslationResult(
            translated_text=translated_text.strip(),
            source_language=source_language,
            target_language=target_language,
            provider=self.provider_name,
            translation_model=self.model,
            confidence_score=0.9,
        )

    def _valid_api_key(self, api_key: str | None) -> str | None:
        if not api_key or api_key.startswith("your_"):
            return None
        return api_key
