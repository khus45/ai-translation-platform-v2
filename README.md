# AI Translation Platform v2

Enterprise-grade AI Translation & Quality Assurance Platform powered by Retrieval-Augmented Generation (RAG), LLMs, AI agents, and human-in-the-loop feedback.

This repository contains the backend and supporting components for a production-ready platform that combines automated translation, context-aware QA, and human review workflows to deliver high-quality localized content at scale.

---

## Key Features

- RAG-enabled retrieval for context-aware translation and QA
- Integration with modern LLMs and AI agents for translation and validation
- Human-in-the-loop feedback to continuously improve model outputs
- Role-based authentication and secure token management
- Test coverage for critical flows (authentication, user management)
- Database migrations using Alembic for reproducible schema changes

---

## What's new

### 2026-08-05 — Authentication & User Management
A secure, production-ready authentication and user management system was added to the backend. Highlights:

- User registration, login, and profile endpoints with input validation and hashed passwords
- Short-lived JWT access tokens and refresh tokens with rotation and refresh token hashing
- Role-based access control (roles: `user`, `admin`) for protected endpoints
- Endpoints: `register`, `login`, `refresh`, `logout`, `users/me`, and admin user listing
- Unit and integration tests for the auth flow: `backend/tests/test_auth_flow.py`
- Alembic migration to add `role` and `refresh_token_hash` to the users table

Commit: https://github.com/khus45/ai-translation-platform-v2/commit/dfb4d7261fa89340ab28277e4e9350cc79677c23

Files changed (highlights):
- backend/app/api/auth.py
- backend/app/api/users.py
- backend/app/services/auth_service.py
- backend/app/services/user_service.py
- backend/app/services/token_service.py
- backend/app/security/jwt.py
- backend/app/security/hashing.py
- backend/app/repositories/user_repository.py
- backend/app/dependencies/auth.py
- backend/app/models/user.py
- backend/.env.example
- backend/migrations/versions/9c1a2b3d4e5f_add_auth_fields_to_users.py
- backend/tests/test_auth_flow.py
- backend/requirements.txt

---

## Quickstart (local development)

Prerequisites:
- Python 3.10+ (or the version pinned in `backend/requirements.txt`)
- PostgreSQL (or the DB configured in your `.env`)
- Optional: Docker & Docker Compose for an isolated setup

1. Copy the example env and update values:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and set SECRET_KEY, DATABASE_URL, and any provider keys (OPENAI_API_KEY, GEMINI_API_KEY) as needed
```

2. Install dependencies and prepare the database:

```bash
cd backend
pip install -r requirements.txt
alembic -c alembic.ini upgrade head
```

3. Run the backend server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Try the basic auth workflow (example):

- Register: POST /api/v1/auth/register { "username": "alice", "email": "alice@example.com", "password": "StrongPass123" }
- Login: POST /api/v1/auth/login -> returns access_token and refresh_token
- Get current user: GET /api/v1/users/me with `Authorization: Bearer <access_token>`
- Refresh: POST /api/v1/auth/refresh { "refresh_token": "<refresh_token>" }

---

## Running tests

Run the unit/integration tests for the backend:

```bash
pytest backend/tests -q
```

To run the auth flow tests specifically:

```bash
pytest backend/tests/test_auth_flow.py -q
```

---

## Deployment notes

- Ensure `SECRET_KEY` and other sensitive environment variables are provided securely (CI secrets, vault, or environment store).
- For production, consider additional strategies for refresh token rotation, revocation, or blacklisting.
- Add provider API keys (OPENAI_API_KEY, GEMINI_API_KEY) to CI/CD secrets if your integration tests or services rely on them.
- Use Docker Compose or Kubernetes for multi-service deployments (DB, backend, optional worker services and queues).

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Open an issue to discuss significant changes or feature requests.
2. Create small, focused pull requests with clear descriptions and tests for new behavior.
3. Run existing tests and add tests for any new functionality.
4. Keep secrets out of commits; use `backend/.env.example` for configuration examples.

---

## Project structure (high level)

- backend/ — FastAPI backend, services, API endpoints, and tests
- backend/migrations/ — Alembic migrations

---

## License

This project does not specify a license in the repository. If this is intended to be open-source, add a LICENSE file (e.g., MIT, Apache-2.0) and update this README.

---

If you’d like, I can also:
- Add a minimal `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` template
- Create a LICENSE file (which license do you prefer?)
- Add example curl requests or Postman collection for the most common API flows

