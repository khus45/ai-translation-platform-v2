class PromptBuilder:
    def build_translation_prompt(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        return (
            "You are a professional translation engine.\n"
            f"Translate the following text from {source_language} "
            f"to {target_language}.\n"
            "Preserve meaning, tone, names, numbers, and formatting.\n"
            "Return only the translated text.\n\n"
            f"Text:\n{source_text}"
        )

    def build_openai_messages(
        self,
        *,
        source_text: str,
        source_language: str,
        target_language: str,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": "You are a precise, production-grade translation engine.",
            },
            {
                "role": "user",
                "content": self.build_translation_prompt(
                    source_text=source_text,
                    source_language=source_language,
                    target_language=target_language,
                ),
            },
        ]
