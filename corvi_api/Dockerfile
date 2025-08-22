# Build with: docker build -f corvi_api/Dockerfile .
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies using Poetry
COPY corvi_api/pyproject.toml /app/corvi_api/pyproject.toml
COPY corvi_api/poetry.lock /app/corvi_api/poetry.lock

RUN pip install --no-cache-dir poetry \
 && cd corvi_api \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy source
COPY corvi_api /app/corvi_api

ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "corvi_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
