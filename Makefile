SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help

include .env
export $(shell sed 's/=.*//' .env)
export PYTHONPATH
export PIPENV_VENV_IN_PROJECT=1

APP_NAME = server:0.1.0
APP_DIR = server
TEST_SRC = $(APP_DIR)/tests

PYTHON := python3
PIP := $(PYTHON) -m pip
PIPENV := $(PYTHON) -m pipenv
DOCKER_COMPOSE_RUN := docker compose exec $(APP_DIR)

POSTGRES_COMMAND := /Applications/Postgres.app/Contents/Versions/latest/bin

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN \
	{FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

### Local commands ###
venv:
	$(PIP) install -U pipenv
	$(PIPENV) shell

install-packages:
	$(PIPENV) install --dev

create-local-database-linux:
	sudo -u postgres psql -c 'create database $(DATABASE_NAME);'
	sudo -u postgres psql -c 'grant all privileges on database $(DATABASE_NAME) \
	to $(DATABASE_USERNAME);'

create-local-database-mac:
	sudo mkdir -p /etc/paths.d && \
  	echo $(POSTGRES_COMMAND) \
  	| sudo tee /etc/paths.d/postgresapp

	sudo $(POSTGRES_COMMAND)/psql -U postgres -c 'create database $(DATABASE_NAME);'
	sudo $(POSTGRES_COMMAND)/psql -U postgres -c 'grant all privileges \
	 on database $(DATABASE_NAME) to $(DATABASE_USERNAME);'

drop-local-database-linux:
	sudo psql -U postgres -c 'drop database $(DATABASE_NAME);'

drop-local-database-mac:
	sudo $(POSTGRES_COMMAND)/psql -U postgres -c 'drop database $(DATABASE_NAME);'

run-local:
	$(PYTHON) -m uvicorn --chdir $(APP_DIR) main:app --reload

makemigrations:
	$(PYTHON) -m alembic $(APP_DIR) revision --autogenerate

migrate:
	$(PYTHON) -m alembic $(APP_DIR) upgrade head

test:
	$(PYTHON) -m pytest $(TEST_SRC)

### Docker commands ###
up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

docker-makemigrations:
	$(DOCKER_COMPOSE_RUN) python3 -m alembic $(APP_DIR) revision --autogenerate -m

docker-migrate:
	$(DOCKER_COMPOSE_RUN) python3 -m alembic $(APP_DIR) upgrade head

copy-env:
	exec cp .env.example .env

docker-test:
	$(DOCKER_COMPOSE_RUN) pytest $(TEST_SRC)

# Consider using test-dev or test-deploy instead
testcov:
	pytest $(tests_src)
	@echo "building coverage html"
	@coverage html
	@echo "opening coverage html in browser"
	@open htmlcov/index.html

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build

.PHONY: help venv install-packages create-local-database-linux
	create-local-database-mac drop-local-database run-local migrate test up down
	test-docker copy-env push-image-aws prod-migrate prod-download-ml-models
	prod-up prod-down logs testcov clean