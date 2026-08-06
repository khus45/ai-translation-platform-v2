from app.services.ai.base_provider import BaseTranslationProvider, TranslationResult
from app.services.prompt_builder import PromptBuilder


class LocalFallbackProvider(BaseTranslationProvider):
    provider_name = "local"

    def __init__(self, prompt_builder: PromptBuilder | None = None):
        self.prompt_builder = prompt_builder or PromptBuilder()

    def translate(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationResult:
        translated_text = self._translate_known_phrase(
            source_text=source_text,
            target_language=target_language,
        )
        return TranslationResult(
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            provider=self.provider_name,
            translation_model="local-fallback-v1",
            confidence_score=0.35,
        )

    def _translate_known_phrase(self, source_text: str, target_language: str) -> str:
        phrase = source_text.strip().lower()
        target = target_language.strip().lower()
        known_phrases = {
            ("hello", "hi"): "नमस्ते",
            ("hello world", "hi"): "नमस्ते दुनिया",
            ("good morning", "hi"): "सुप्रभात",
            ("thank you", "hi"): "धन्यवाद",
            ("how are you?", "hi"): "आप कैसे हैं?",
            ("how are you", "hi"): "आप कैसे हैं?",
            ("नमस्ते", "en"): "Hello",
            ("धन्यवाद", "en"): "Thank you",
        }
        if (phrase, target) in known_phrases:
            return known_phrases[(phrase, target)]
        return f"[{target_language}] {source_text}"
