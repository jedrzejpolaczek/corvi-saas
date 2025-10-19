#!/bin/sh
alembic -c /app/corvi_api/alembic.ini upgrade head
exec uvicorn corvi_api.app:app --host 0.0.0.0 --port 8000