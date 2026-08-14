run:
	docker compose up

run-dev:
	cd backend && DATABASE_URL=postgresql://postgres:postgres@localhost:5432/translation_db DEFAULT_TRANSLATION_PROVIDER=local venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

down:
	docker compose down

build:
	docker compose build

format:
	black backend

lint:
	ruff check backend

test:
	PYTHONPATH=backend backend/venv/bin/python -m pytest backend/tests -q

smoke:
	./scripts/smoke_test.sh
