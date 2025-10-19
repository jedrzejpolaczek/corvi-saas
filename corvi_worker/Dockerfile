# Build with: docker build -f corvi_worker/Dockerfile .
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install API and Worker deps via Poetry (worker reuses API models)
COPY corvi_api/pyproject.toml /app/corvi_api/pyproject.toml
COPY corvi_api/poetry.lock /app/corvi_api/poetry.lock
COPY corvi_worker/pyproject.toml /app/corvi_worker/pyproject.toml
COPY corvi_worker/poetry.lock /app/corvi_worker/poetry.lock

RUN pip install --no-cache-dir poetry \
 && cd corvi_api \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi \
 && cd ../corvi_worker \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy sources
COPY corvi_api /app/corvi_api
COPY corvi_worker /app/corvi_worker

ENV PYTHONPATH=/app

CMD ["python", "-m", "corvi_worker.runner"]
