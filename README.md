# Enterprise AI Translation Intelligence Platform

A production-style AI platform for translation, translation quality review, RAG-based context retrieval, multi-agent evaluation, human feedback, and analytics.

Most translation tools only translate text. They do not answer whether the meaning is preserved, grammar is correct, terminology is consistent, information is missing, or a human reviewer should approve the result. This project solves that problem by combining AI translation, retrieval, quality agents, evaluation metrics, and human-in-the-loop feedback.

## Highlights

- JWT authentication with access and refresh tokens
- Role-based protected APIs
- AI translation engine with provider pattern
- OpenAI, Gemini, and local fallback providers
- Language and domain detection
- Glossary-based RAG context
- Translation memory
- Multi-agent QA pipeline
- Grammar, terminology, hallucination, and reviewer agents
- Evaluation metrics: semantic similarity, ChrF-style score, BLEU-lite
- Human feedback workflow
- Analytics summary API
- Frontend dashboard
- JSON and CSV export
- Docker Compose setup
- GitHub Actions CI
- PostgreSQL, Redis, Qdrant, Prometheus, and Grafana service definitions

## Architecture

```text
User
  |
Frontend Dashboard
  |
FastAPI Backend
  |
  |-- Auth Service
  |-- Translation Service
  |-- Provider Factory
  |     |-- OpenAI Provider
  |     |-- Gemini Provider
  |     |-- Local Fallback Provider
  |
  |-- RAG Service
  |     |-- Glossary
  |     |-- Translation Memory
  |
  |-- QA Agents
  |     |-- Grammar Agent
  |     |-- Terminology Agent
  |     |-- Hallucination Agent
  |     |-- Reviewer Agent
  |
  |-- Evaluation Service
  |-- Feedback Service
  |-- Analytics Service
  |
PostgreSQL / Redis / Qdrant
```

## Tech Stack

| Area | Tools |
| --- | --- |
| Backend | FastAPI, Python, Pydantic |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Auth | JWT, password hashing, RBAC |
| AI Providers | OpenAI SDK, Gemini SDK, local fallback |
| AI Architecture | Provider pattern, RAG-style retrieval, multi-agent QA |
| Evaluation | Semantic similarity, ChrF-style score, BLEU-lite |
| Frontend | HTML, CSS, JavaScript dashboard |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Monitoring Surface | Prometheus, Grafana |

## Project Structure

```text
ai-translation-platform-v2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── security/
│   │   └── services/
│   ├── migrations/
│   └── tests/
├── frontend/
│   ├── index.html
│   └── src/
├── docs/
├── docker/
├── scripts/
├── .github/workflows/
├── docker-compose.yml
└── Makefile
```

## Core API Endpoints

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/me`

### Translation

- `POST /api/v1/translate`
- `POST /api/v1/translate/stream`
- `POST /api/v1/detect-language`
- `GET /api/v1/translations`
- `GET /api/v1/translations/{translation_id}`
- `DELETE /api/v1/translations/{translation_id}`
- `GET /api/v1/translations/export/json`
- `GET /api/v1/translations/export/csv`

### AI Intelligence

- `POST /api/v1/qa/review`
- `GET /api/v1/qa/reports`
- `POST /api/v1/glossary`
- `GET /api/v1/glossary`
- `GET /api/v1/translation-memory`
- `POST /api/v1/translations/{translation_id}/feedback`
- `POST /api/v1/documents/ingest`
- `GET /api/v1/documents`
- `GET /api/v1/analytics/summary`

## Run Locally

### 1. Start Infrastructure

```bash
docker compose up -d postgres redis qdrant
```

### 2. Run Backend

```bash
cd backend
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db venv/bin/alembic upgrade head
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db DEFAULT_TRANSLATION_PROVIDER=local venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend docs:

```text
http://127.0.0.1:8000/docs
```

### 3. Run Frontend

Open a second terminal:

```bash
cd frontend
python3 -m http.server 5173
```

Frontend:

```text
http://127.0.0.1:5173
```

## Run With Docker Compose

```bash
docker compose up --build
```

Services:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- Qdrant: `http://127.0.0.1:6333`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`

## Verification

```bash
backend/venv/bin/python -m ruff check backend
```

```bash
PYTHONPATH=backend backend/venv/bin/python -m pytest backend/tests -q
```

```bash
./scripts/smoke_test.sh
```

Expected:

```text
All checks passed
7 passed
Smoke test passed
```

## Example Workflow

1. Register a user.
2. Add a glossary term.
3. Translate source text.
4. Retrieve RAG context from glossary and translation memory.
5. Run QA review.
6. Generate grammar, terminology, hallucination, fluency, and confidence scores.
7. Approve or reject translation with human feedback.
8. Update translation memory.
9. View analytics summary.
10. Export translation history as JSON or CSV.

## Why This Project Is Portfolio-Worthy

This project demonstrates practical AI engineering and backend system design:

- Production API architecture with FastAPI
- Authentication, RBAC, and protected routes
- AI provider abstraction for multiple LLM providers
- RAG-style context retrieval
- Translation memory for localization workflows
- Multi-agent quality review
- Evaluation metrics and explainable scoring
- Human feedback loop
- Analytics-ready data model
- Full-stack runnable dashboard
- Dockerized development workflow
- CI pipeline with GitHub Actions

## Current Scope

The project is fully runnable locally and designed as a strong portfolio MVP. Some production integrations are intentionally represented as integration surfaces or placeholders:

- Google and Microsoft OAuth endpoints are placeholders until OAuth credentials are configured.
- OCR and speech workflows are represented by document text ingestion.
- Qdrant, Redis, Prometheus, and Grafana are available in Docker Compose for expansion.
- Real OpenAI and Gemini calls require API keys; local fallback works without keys.

## Environment Variables

See:

```text
backend/.env.example
```

Important values:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEFAULT_TRANSLATION_PROVIDER`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `CORS_ALLOW_ORIGINS`

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Database](docs/database.md)
- [Deployment](docs/deployment.md)

## Future Improvements

- Real OCR pipeline for PDF and image uploads
- Whisper-based speech translation
- Real Qdrant vector embeddings
- COMET and BERTScore integration
- Google and Microsoft OAuth implementation
- Advanced React or Next.js dashboard
- AWS deployment with Nginx and SSL
