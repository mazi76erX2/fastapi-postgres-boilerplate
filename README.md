# fastapi-postgres-boilerplate

FastAPI boilerplate with PostgreSQL, Redis, Alembic, and modern Python tooling.

## Stack

- FastAPI
- SQLAlchemy 2.0 (async + asyncpg)
- Alembic
- Redis
- uv (package + environment management)
- Ruff + MyPy + Pytest

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Local development

1. Copy env file:

	 ```bash
	 cp .env.example .env
	 ```

2. Create environment and install dependencies:

	 ```bash
	 uv venv
	 uv sync --all-extras
	 ```

3. Run migrations:

	 ```bash
	 uv run alembic upgrade head
	 ```

4. Start API:

	 ```bash
	 uv run uvicorn main:app --app-dir server --reload
	 ```

## Quality checks

- Format:

	```bash
	uv run ruff format .
	```

- Lint:

	```bash
	uv run ruff check .
	```

- Type check:

	```bash
	uv run mypy server
	```

- Tests:

	```bash
	uv run pytest
	```

## Docker

- Development:

	```bash
	docker compose up -d --build
	```

- Production compose:

	```bash
	docker compose -f docker-compose.prod.yml up -d --build
	```

Both containers run Alembic migrations on startup and then launch Uvicorn.
