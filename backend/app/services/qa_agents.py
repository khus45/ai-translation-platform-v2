from dataclasses import dataclass


@dataclass(frozen=True)
class AgentFinding:
    score: float
    errors: list[str]
    suggestions: list[str]


class GrammarAgent:
    def review(self, translated_text: str) -> AgentFinding:
        errors = []
        suggestions = []
        score = 94.0
        if translated_text != translated_text.strip():
            errors.append("Leading or trailing whitespace detected")
            suggestions.append("Trim whitespace before delivery")
            score -= 8
        if "  " in translated_text:
            errors.append("Repeated spacing found")
            suggestions.append("Normalize repeated spaces")
            score -= 6
        if not translated_text:
            errors.append("Translation is empty")
            suggestions.append("Provide a translated sentence")
            score = 0
        return AgentFinding(max(score, 0), errors, suggestions)


class TerminologyAgent:
    def review(self, missing_terms: list[str]) -> AgentFinding:
        if not missing_terms:
            return AgentFinding(96.0, [], ["Terminology is consistent with glossary"])
        return AgentFinding(
            max(40.0, 96.0 - len(missing_terms) * 18),
            [f"Glossary term not followed: {term}" for term in missing_terms],
            ["Use approved glossary translations for highlighted terms"],
        )


class HallucinationAgent:
    NEGATION_PAIRS = [
        ("failed", "successful"),
        ("successfully", "failed"),
        ("approved", "rejected"),
        ("rejected", "approved"),
        ("cancel", "confirm"),
    ]

    def review(self, source_text: str, translated_text: str) -> AgentFinding:
        source = source_text.lower()
        translation = translated_text.lower()
        errors = []
        for source_word, conflicting_word in self.NEGATION_PAIRS:
            if source_word in source and conflicting_word in translation:
                errors.append(
                    "Potential meaning contradiction: "
                    f"{source_word} vs {conflicting_word}"
                )
        length_gap = abs(len(source_text) - len(translated_text)) / max(
            len(source_text), 1
        )
        if length_gap > 2.5:
            errors.append("Translation length differs unusually from source")

        score = max(0.0, 98.0 - len(errors) * 35.0)
        suggestions = []
        if errors:
            suggestions.append("Re-check meaning preservation against the source")
        return AgentFinding(score, errors, suggestions)


class ReviewerAgent:
    def summarize(
        self,
        *,
        grammar: AgentFinding,
        terminology: AgentFinding,
        hallucination: AgentFinding,
        metrics: dict,
    ) -> dict:
        fluency_score = round((grammar.score + metrics["chrf"] * 100) / 2, 2)
        meaning_score = round(
            (hallucination.score + metrics["semantic_similarity"] * 100) / 2,
            2,
        )
        overall_score = round(
            (
                grammar.score
                + meaning_score
                + terminology.score
                + fluency_score
                + hallucination.score
            )
            / 5,
            2,
        )
        confidence_score = round(min(99.0, max(1.0, overall_score * 0.98)), 2)
        return {
            "grammar_score": round(grammar.score, 2),
            "meaning_score": meaning_score,
            "terminology_score": round(terminology.score, 2),
            "fluency_score": fluency_score,
            "hallucination_score": round(hallucination.score, 2),
            "overall_score": overall_score,
            "confidence_score": confidence_score,
        }
