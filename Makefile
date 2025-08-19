.PHONY: run worker test fmt lint

run:
	uvicorn app.main:app --reload

worker:
	celery -A app.workers.celery_app.celery worker --loglevel=INFO

test:
	pytest -q

fmt:
	python -m pip install ruff black
	ruff check --fix .
	black .

lint:
	ruff check .
