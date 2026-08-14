from dataclasses import dataclass


@dataclass(frozen=True)
class DomainDetectionResult:
    domain: str
    confidence_score: float


class DomainDetectionService:
    KEYWORDS = {
        "medical": {"doctor", "medicine", "patient", "diagnosis", "prescription"},
        "legal": {"contract", "clause", "court", "agreement", "liability"},
        "finance": {"payment", "invoice", "bank", "refund", "tax", "transaction"},
        "technical": {"api", "server", "database", "deploy", "latency", "token"},
        "ecommerce": {"order", "cart", "shipment", "delivery", "return"},
    }

    def detect(self, text: str) -> DomainDetectionResult:
        lowered = text.lower()
        scores = {
            domain: sum(1 for keyword in keywords if keyword in lowered)
            for domain, keywords in self.KEYWORDS.items()
        }
        domain, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            return DomainDetectionResult(domain="general", confidence_score=0.55)
        return DomainDetectionResult(
            domain=domain,
            confidence_score=min(0.65 + score * 0.1, 0.95),
        )
