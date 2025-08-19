from app.workers.tasks import run_experiment

def enqueue_experiment(experiment_id: int) -> None:
    # Send to Celery
    run_experiment.delay(experiment_id)
