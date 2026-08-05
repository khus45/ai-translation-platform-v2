# ai-translation-platform-v2
Enterprise-grade AI Translation & Quality Assurance Platform powered by RAG, LLMs, AI Agents, and Human-in-the-Loop Feedback.

## What's new

### 2026-08-05 — Added authentication & user management
- Summary: Implemented user registration, login, refresh/logout, JWT access/refresh tokens, password hashing, role-based access control, and user listing APIs.
- Files changed (highlights):
  - backend/app/api/auth.py (new)
  - backend/app/api/users.py (new)
  - backend/app/services/auth_service.py (new)
  - backend/app/services/user_service.py (new)
  - backend/app/services/token_service.py (new)
  - backend/app/security/jwt.py (new)
  - backend/app/security/hashing.py (new)
  - backend/app/repositories/user_repository.py (new)
  - backend/app/dependencies/auth.py (new)
  - backend/app/models/user.py (updated)
  - backend/app/config/settings.py (updated)
  - backend/.env.example (updated)
  - backend/migrations/versions/9c1a2b3d4e5f_add_auth_fields_to_users.py (new)
  - backend/tests/test_auth_flow.py (new)
  - backend/requirements.txt (updated)
- Tests: Added unit/integration tests at `backend/tests/test_auth_flow.py` covering register/login/refresh/me and admin role checks.
- DB / Migrations: Added Alembic migration to add `role` and `refresh_token_hash` columns to `users` (see backend/migrations/versions/9c1a2b3d4e5f_add_auth_fields_to_users.py).

How to verify:
1. Ensure environment variables are set (see `backend/.env.example`) — SECRET_KEY and token settings were added.
2. Run services: `docker-compose up --build` or run the backend directly:
   ```bash
   cd backend
   # optional: create venv and install deps
   pip install -r requirements.txt
   alembic -c alembic.ini upgrade head
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Exercise the API:
   - Register: POST /api/v1/auth/register { username, email, password }
   - Login: POST /api/v1/auth/login (form) -> receive access_token and refresh_token
   - Inspect current user: GET /api/v1/users/me with Authorization: Bearer <access_token>
   - Refresh token: POST /api/v1/auth/refresh { refresh_token }
4. Run the new tests:
   ```bash
   pytest backend/tests/test_auth_flow.py -q
   ```

Notes / follow-ups:
- Add CI secrets for any external AI providers (OPENAI_API_KEY, GEMINI_API_KEY) if tests or services require them.
- Consider rotating secrets and storing refresh tokens securely in production.
- Add integration tests for the full Docker Compose setup.
