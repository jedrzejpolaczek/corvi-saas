from __future__ import annotations
import json, math, os, random, tempfile, time
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.workers.celery_app import celery
from app.config import settings
from app.models import SessionLocal
from app.models.models import Experiment, Dataset, Trial
from app.services.s3 import s3_client

RNG = np.random.default_rng()

def _prepare_xy(df: pd.DataFrame, task_type: str):
    # Heuristic: if 'target' column present, use it; else last column.
    target_col = "target" if "target" in df.columns else df.columns[-1]
    y = df[target_col].values
    X = df.drop(columns=[target_col]).values
    return X, y, target_col

def _sample_params(task_type: str) -> dict[str, Any]:
    if task_type == "classification":
        # Logistic Regression: C ~ log-uniform [1e-2, 1e1]
        C = float(np.exp(RNG.uniform(np.log(1e-2), np.log(1e1))))
        max_iter = int(RNG.integers(100, 600))
        return {"C": C, "max_iter": max_iter, "solver": "liblinear"}
    else:
        # Regression: Ridge alpha ~ log-uniform
        alpha = float(np.exp(RNG.uniform(np.log(1e-3), np.log(10.0))))
        return {"alpha": alpha}

def _fit_and_score(task_type: str, X_train, X_test, y_train, y_test, params: dict[str, Any]):
    if task_type == "classification":
        model = LogisticRegression(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        metric = accuracy_score(y_test, preds)
        return metric, "accuracy"
    else:
        model = Ridge(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        metric = r2_score(y_test, preds)
        return metric, "r2"

@celery.task(name="app.run_experiment")
def run_experiment(experiment_id: int) -> None:
    db: Session = SessionLocal()
    try:
        exp: Experiment | None = db.get(Experiment, experiment_id)
        if not exp:
            return
        if exp.status in ("running", "finished", "stopped"):
            return

        exp.status = "running"
        exp.started_at = datetime.utcnow()
        db.commit()
        db.refresh(exp)

        # Download dataset
        ds: Dataset = db.get(Dataset, exp.dataset_id)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        tmp.close()
        s3_client.download_to_path(ds.s3_key, tmp.name)
        df = pd.read_csv(tmp.name)
        os.unlink(tmp.name)

        X, y, target_col = _prepare_xy(df, exp.task_type)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        best_so_far: float | None = None
        trials_done = 0
        last_improve_trial = -1
        recent_window = []  # record last K metrics
        t_start = time.time()

        min_useful = settings.CLASSIFICATION_MIN_USEFUL if exp.task_type == "classification" else settings.REGRESSION_MIN_USEFUL

        for t in range(exp.budget_trials):
            db.refresh(exp)  # pick up stop flag
            if exp.stop_requested:
                exp.status = "stopped"
                exp.ended_at = datetime.utcnow()
                db.commit()
                return

            if (time.time() - t_start) >= exp.time_limit_minutes * 60:
                exp.status = "stopped"
                exp.ended_at = datetime.utcnow()
                db.commit()
                return

            params = _sample_params(exp.task_type)
            t0 = time.time()
            try:
                metric, metric_name = _fit_and_score(exp.task_type, X_train, X_test, y_train, y_test, params)
                duration = time.time() - t0
                trials_done += 1
                best_so_far = metric if (best_so_far is None or metric > best_so_far) else best_so_far

                # Record trial
                trial = Trial(
                    experiment_id=exp.id,
                    params=params,
                    metric_name=metric_name,
                    metric_value=float(metric),
                    early_stopped=False,
                    duration_s=float(duration),
                )
                db.add(trial)
                db.commit()

                # First useful result
                if exp.first_result_time_s is None:
                    if metric >= min_useful or trials_done == 1:
                        exp.first_result_time_s = time.time() - t_start
                        exp.first_result_trials_used = trials_done
                        exp.first_result_metric_name = metric_name
                        exp.first_result_metric_value = float(metric)
                        db.commit()

                # Pruning/early-stop MVP
                recent_window.append(metric)
                if len(recent_window) > settings.PRUNING_LAST_K:
                    recent_window.pop(0)
                # If no improvement greater than min_delta in last K
                if len(recent_window) == settings.PRUNING_LAST_K:
                    if (max(recent_window) - min(recent_window)) < settings.PRUNING_MIN_DELTA:
                        # Stop early
                        exp.status = "finished"
                        exp.ended_at = datetime.utcnow()
                        db.commit()
                        return

            except Exception:
                # Record failed trial
                duration = time.time() - t0
                trial = Trial(
                    experiment_id=exp.id,
                    params=params,
                    metric_name="error",
                    metric_value=None,
                    early_stopped=True,
                    duration_s=float(duration),
                )
                db.add(trial)
                db.commit()
                continue

        exp.status = "finished"
        exp.ended_at = datetime.utcnow()
        db.commit()

    except Exception:
        # Mark failed experiment
        exp = db.get(Experiment, experiment_id)
        if exp:
            exp.status = "failed"
            exp.ended_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()
