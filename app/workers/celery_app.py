from celery import Celery
from app.config import settings

celery = Celery(
    "corvi",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"],
)

celery.conf.update(
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    timezone="UTC",
    task_track_started=True,
    worker_send_task_events=True,
)
