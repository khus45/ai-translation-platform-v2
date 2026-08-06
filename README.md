# ai-translation-platform-v2
Enterprise-grade AI Translation & Quality Assurance Platform powered by RAG, LLMs, AI Agents, and Human-in-the-Loop Feedback.

## What's new

### 2026-08-05 — Authentication & User Management
- Overview: Added a secure, production-ready authentication and user management system to the backend. This includes user registration, login, JWT access and refresh tokens, secure password hashing, role-based access control (RBAC), and admin-only user listing.
- Key features:
  - User registration and login endpoints with hashed passwords and validation.
  - Short-lived JWT access tokens and longer-lived refresh tokens for session management.
  - Refresh token rotation and storage of refresh token hashes to reduce risk from token leakage.
  - Role-based access control with `user` and `admin` roles for protected endpoints.
  - Endpoints: register, login, refresh, logout, get current user, and admin user listing.
- Tests: Added unit/integration tests covering the auth flow (register, login, refresh, /users/me) and admin checks: `backend/tests/test_auth_flow.py`.
- Database / Migrations: Alembic migration added to extend the users table with `role` and `refresh_token_hash` columns.
- Commit: https://github.com/khus45/ai-translation-platform-v2/commit/dfb4d7261fa89340ab28277e4e9350cc79677c23
- Files changed (highlights):
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/api/auth.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/api/users.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/services/auth_service.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/services/user_service.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/services/token_service.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/security/jwt.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/security/hashing.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/repositories/user_repository.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/dependencies/auth.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/app/models/user.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/.env.example
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/migrations/versions/9c1a2b3d4e5f_add_auth_fields_to_users.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/tests/test_auth_flow.py
  - https://github.com/khus45/ai-translation-platform-v2/blob/main/backend/requirements.txt

How to verify (quick):
1. Ensure required environment variables are set (see `backend/.env.example`) — especially SECRET_KEY and token settings.
2. Start the backend (Docker or locally):
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic -c alembic.ini upgrade head
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. API workflow examples:
   - Register: POST /api/v1/auth/register { username, email, password }
   - Login: POST /api/v1/auth/login (form) -> receive access_token and refresh_token
   - Inspect current user: GET /api/v1/users/me with `Authorization: Bearer <access_token>`
   - Refresh token: POST /api/v1/auth/refresh { refresh_token }
4. Run the tests for the new flow:
   ```bash
   pytest backend/tests/test_auth_flow.py -q
   ```

Notes & next steps:
- Add CI secrets for external providers (OPENAI_API_KEY, GEMINI_API_KEY) if integration tests or services require them.
- Securely manage SECRET_KEY and consider refresh token rotation/blacklisting strategies in production.
- Consider adding integration tests that run the full Docker Compose stack and end-to-end authentication scenarios.
- Optionally document admin role usage and any CLI or administrative tooling to manage users.
