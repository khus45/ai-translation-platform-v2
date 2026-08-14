from difflib import SequenceMatcher


class EvaluationService:
    def evaluate(
        self,
        *,
        source_text: str,
        translated_text: str,
        glossary_hits: int = 0,
        missing_terms: int = 0,
    ) -> dict:
        semantic_similarity = self._similarity(source_text, translated_text)
        length_ratio = self._length_ratio(source_text, translated_text)
        chrf = self._character_f_score(source_text, translated_text)
        bleu_lite = self._bleu_lite(source_text, translated_text)
        terminology_score = max(0.0, 100.0 - missing_terms * 18.0)
        if glossary_hits and missing_terms == 0:
            terminology_score = 100.0

        return {
            "semantic_similarity": round(semantic_similarity, 4),
            "length_ratio": round(length_ratio, 4),
            "chrf": round(chrf, 4),
            "bleu_lite": round(bleu_lite, 4),
            "terminology_score": round(terminology_score, 2),
        }

    def _similarity(self, left: str, right: str) -> float:
        return SequenceMatcher(None, left.lower(), right.lower()).ratio()

    def _length_ratio(self, left: str, right: str) -> float:
        if not left:
            return 0.0
        return min(len(right) / len(left), len(left) / max(len(right), 1))

    def _character_f_score(self, left: str, right: str) -> float:
        left_chars = set(left.lower())
        right_chars = set(right.lower())
        if not left_chars or not right_chars:
            return 0.0
        precision = len(left_chars & right_chars) / len(right_chars)
        recall = len(left_chars & right_chars) / len(left_chars)
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def _bleu_lite(self, left: str, right: str) -> float:
        left_words = left.lower().split()
        right_words = right.lower().split()
        if not left_words or not right_words:
            return 0.0
        overlap = len(set(left_words) & set(right_words))
        precision = overlap / len(set(right_words))
        brevity = min(1.0, len(right_words) / len(left_words))
        return precision * brevity
