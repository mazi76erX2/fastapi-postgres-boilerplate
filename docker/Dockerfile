FROM python:3.14-slim

ENV TZ=UTC+2
ENV UV_SYSTEM_PYTHON=1

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    libpq5 \
    libpq-dev \
    build-essential \
    curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip uv

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --all-extras || uv sync --all-extras --upgrade

COPY . .
RUN chmod +x /app/docker/entrypoint.sh

ENTRYPOINT ["/app/docker/entrypoint.sh"]
