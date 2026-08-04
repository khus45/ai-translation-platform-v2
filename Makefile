run:
	docker compose up

down:
	docker compose down

build:
	docker compose build

format:
	black backend

lint:
	ruff check backend

test:
	pytest