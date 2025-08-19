# Corvi Backend API + Worker (MVP HPO)

FastAPI + Celery MVP that accepts datasets, launches random-search HPO experiments with lightweight pruning/early-stop, and reports the **first useful result**.

## Stack
- Python 3.11
- FastAPI, Uvicorn, Pydantic v2
- SQLAlchemy 2.x, Alembic
- Celery + Redis (broker/backend)
- S3/MinIO via `boto3`
- Optional: `numpy`, `pandas`, `scikit-learn` for pseudo-training

## Structure
```
app/
  main.py
  config.py
  security.py
  deps.py
  models/
  routers/
  services/
  workers/
  schemas/
  instrumentation/
  tests/
requirements.txt
.env.example
Makefile
```
## Endpoints
- `POST /auth/register` – register user
- `POST /auth/login` – login, returns `{access_token}`
- `POST /datasets/upload` – multipart CSV upload → S3 key + DB record
- `POST /experiments` – create experiment (queued) and enqueue Celery task
- `GET /experiments` – list user's experiments
- `GET /experiments/{id}` – details incl. trials + first useful result
- `GET /experiments/{id}/status` – {status, progress_pct, eta_s}
- `PATCH /experiments/{id}/stop` – request stop (worker respects)

## Run (dev)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# .env
cp .env.example .env

# API
uvicorn app.main:app --reload

# Celery worker
celery -A app.workers.celery_app.celery worker --loglevel=INFO
```

## Env
See `.env.example`. For MinIO:
- `S3_ENDPOINT_URL=http://localhost:9000`
- `S3_ACCESS_KEY`, `S3_SECRET_KEY`
- Create bucket `corvi-datasets` or let the service auto-create.

## Notes
- First useful result threshold: 0.60 for classification (accuracy), 0.30 for regression (R²). Configurable in `config.py`.
- Early-stop: stop if last K metrics vary < `PRUNING_MIN_DELTA` (flat progress). Also respects time limit & stop flag.
- For proper DB migrations, add Alembic and generate migrations from models.

## Tests
```bash
pytest -q
```
Tests run Celery in eager mode and monkeypatch S3 to local files.
