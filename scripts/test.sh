#!/bin/bash
set -e

uv run pytest --cov=server
