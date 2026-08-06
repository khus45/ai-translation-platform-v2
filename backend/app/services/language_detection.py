from dataclasses import dataclass
from unicodedata import name


@dataclass(frozen=True)
class LanguageDetectionResult:
    language: str
    confidence_score: float


class LanguageDetectionService:
    def detect(self, text: str) -> LanguageDetectionResult:
        normalized = text.strip()
        if not normalized:
            return LanguageDetectionResult(language="unknown", confidence_score=0.0)

        if self._contains_script(normalized, "DEVANAGARI"):
            return LanguageDetectionResult(language="hi", confidence_score=0.92)
        if self._contains_script(normalized, "ARABIC"):
            return LanguageDetectionResult(language="ar", confidence_score=0.9)
        if self._contains_script(normalized, "CYRILLIC"):
            return LanguageDetectionResult(language="ru", confidence_score=0.88)
        if self._contains_script(normalized, "HIRAGANA") or self._contains_script(
            normalized,
            "KATAKANA",
        ):
            return LanguageDetectionResult(language="ja", confidence_score=0.88)
        if self._contains_script(normalized, "CJK"):
            return LanguageDetectionResult(language="zh", confidence_score=0.86)

        ascii_letters = sum(
            character.isascii() and character.isalpha() for character in normalized
        )
        total_letters = sum(character.isalpha() for character in normalized)
        if total_letters and ascii_letters / total_letters > 0.8:
            return LanguageDetectionResult(language="en", confidence_score=0.78)

        return LanguageDetectionResult(language="unknown", confidence_score=0.35)

    def _contains_script(self, text: str, script: str) -> bool:
        return any(script in name(character, "") for character in text)
