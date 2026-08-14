from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.intelligence_repository import (
    GlossaryRepository,
    TranslationMemoryRepository,
)


class RAGService:
    def __init__(self, db: Session):
        self.glossary_repository = GlossaryRepository(db)
        self.memory_repository = TranslationMemoryRepository(db)

    def retrieve_context(
        self,
        *,
        user: User,
        source_text: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> list[dict]:
        glossary_terms = self.glossary_repository.search_relevant(
            user_id=user.id,
            text=source_text,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
        )
        memories = self.memory_repository.search_similar(
            user_id=user.id,
            source_text=source_text,
            source_language=source_language,
            target_language=target_language,
        )

        context = [
            {
                "type": "glossary",
                "term": term.term,
                "approved_translation": term.approved_translation,
                "domain": term.domain,
            }
            for term in glossary_terms
        ]
        context.extend(
            {
                "type": "translation_memory",
                "source_text": memory.source_text,
                "translated_text": memory.translated_text,
                "quality_score": memory.quality_score,
            }
            for memory in memories
        )
        return context

    def glossary_term_gaps(
        self,
        *,
        source_text: str,
        translated_text: str,
        context: list[dict],
    ) -> list[str]:
        lowered_source = source_text.lower()
        lowered_translation = translated_text.lower()
        missing = []
        for item in context:
            if item.get("type") != "glossary":
                continue
            term = str(item["term"]).lower()
            approved = str(item["approved_translation"]).lower()
            if term in lowered_source and approved not in lowered_translation:
                missing.append(item["term"])
        return missing
