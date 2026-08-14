# Database

Main tables:

- `users`
- `translations`
- `translation_memory`
- `glossary_terms`
- `quality_reports`
- `feedback`
- `documents`

Run migrations:

```bash
cd backend
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db venv/bin/alembic upgrade head
```
