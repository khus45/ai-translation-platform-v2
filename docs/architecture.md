# Architecture

The platform is a FastAPI + PostgreSQL backend with a lightweight dashboard UI.

Core backend modules:

- Auth and RBAC with JWT access/refresh tokens
- Translation provider pattern for local, OpenAI, Gemini, and future providers
- RAG-style context retrieval from glossary and translation memory
- Multi-agent QA pipeline for grammar, terminology, hallucination, and reviewer scoring
- Evaluation metrics for semantic similarity, ChrF-style score, BLEU-lite, and confidence
- Human feedback loop that updates translation memory
- Analytics summary for dashboard reporting

Local dependencies:

- PostgreSQL for relational data
- Redis service placeholder for caching workflows
- Qdrant service placeholder for vector database workflows
- Prometheus and Grafana containers for monitoring expansion
