from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.deps import db_session, current_user
from app.schemas.experiments import ExperimentCreate, ExperimentOut, TrialOut, ExperimentStatusOut, FirstUsefulResult
from app.models.models import Experiment, Trial, Dataset, User
from app.services.hpo_runner import enqueue_experiment

router = APIRouter(prefix="/experiments", tags=["experiments"])

@router.post("", response_model=ExperimentOut, status_code=201)
def create_experiment(payload: ExperimentCreate, db: Session = Depends(db_session), user: User = Depends(current_user)):
    ds = db.query(Dataset).filter(Dataset.id == payload.dataset_id, Dataset.user_id == user.id).first()
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found or not owned by user")
    exp = Experiment(
        user_id=user.id,
        dataset_id=ds.id,
        task_type=payload.task_type,
        objective_metric=payload.objective_metric,
        budget_trials=payload.budget_trials,
        time_limit_minutes=payload.time_limit_minutes,
        status="queued",
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)

    enqueue_experiment(exp.id)
    return to_experiment_out(exp, db)

@router.get("", response_model=list[ExperimentOut])
def list_experiments(db: Session = Depends(db_session), user: User = Depends(current_user)):
    exps = db.query(Experiment).filter(Experiment.user_id == user.id).order_by(Experiment.created_at.desc()).all()
    return [to_experiment_out(e, db) for e in exps]

@router.get("/{exp_id}", response_model=ExperimentOut)
def get_experiment(exp_id: int, db: Session = Depends(db_session), user: User = Depends(current_user)):
    exp = db.query(Experiment).filter(Experiment.id == exp_id, Experiment.user_id == user.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return to_experiment_out(exp, db)

@router.get("/{exp_id}/status", response_model=ExperimentStatusOut)
def get_status(exp_id: int, db: Session = Depends(db_session), user: User = Depends(current_user)):
    exp = db.query(Experiment).filter(Experiment.id == exp_id, Experiment.user_id == user.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    total = exp.budget_trials
    done = db.query(func.count(Trial.id)).filter(Trial.experiment_id == exp.id).scalar() or 0
    progress = (done / total) * 100 if total > 0 else 0.0

    # ETA: avg duration * remaining
    durations = db.query(Trial.duration_s).filter(Trial.experiment_id == exp.id, Trial.duration_s != None).all()  # noqa: E711
    avg = sum(d[0] for d in durations) / len(durations) if durations else None
    remaining = max(total - done, 0)
    eta = (avg * remaining) if (avg is not None and exp.status in ("queued", "running")) else None

    return ExperimentStatusOut(status=exp.status, progress_pct=round(progress, 2), eta_s=eta if eta else None)

@router.patch("/{exp_id}/stop")
def stop_experiment(exp_id: int, db: Session = Depends(db_session), user: User = Depends(current_user)):
    exp = db.query(Experiment).filter(Experiment.id == exp_id, Experiment.user_id == user.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    exp.stop_requested = True
    db.commit()
    return {"status": "stop_requested"}

def to_experiment_out(exp: Experiment, db: Session) -> ExperimentOut:
    trials = db.query(Trial).filter(Trial.experiment_id == exp.id).order_by(Trial.created_at.asc()).all()
    first = None
    if exp.first_result_time_s is not None:
        first = FirstUsefulResult(
            time_to_result_s=exp.first_result_time_s,
            trials_used=exp.first_result_trials_used or 0,
            metric_name=exp.first_result_metric_name or exp.objective_metric,
            metric_value=exp.first_result_metric_value or 0.0,
        )
    return ExperimentOut(
        id=exp.id,
        status=exp.status,
        created_at=exp.created_at,
        first_useful_result=first,
        task_type=exp.task_type,
        objective_metric=exp.objective_metric,
        budget_trials=exp.budget_trials,
        time_limit_minutes=exp.time_limit_minutes,
        trials=[TrialOut.model_validate(t) for t in trials],
    )
