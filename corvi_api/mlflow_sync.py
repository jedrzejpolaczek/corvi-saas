import mlflow
from .config import settings
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

def log_metric(run_name: str, key: str, value: float, step: int | None = None):
    with mlflow.start_run(run_name=run_name, nested=True) as run:
        mlflow.log_metric(key, value, step=step)
    return True
