#!/bin/bash
set -e

uv run ruff format --check .
uv run ruff check .
uv run mypy server
