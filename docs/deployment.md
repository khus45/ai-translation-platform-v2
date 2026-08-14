# Deployment

Local full stack:

```bash
docker compose up --build
```

Local backend only:

```bash
docker compose up -d postgres redis qdrant
cd backend
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db venv/bin/alembic upgrade head
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db DEFAULT_TRANSLATION_PROVIDER=local venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```text
http://127.0.0.1:5173
```

Backend docs:

```text
http://127.0.0.1:8000/docs
```
