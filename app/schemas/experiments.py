from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class ExperimentCreate(BaseModel):
    dataset_id: int
    task_type: str
    objective_metric: str
    budget_trials: int
    time_limit_minutes: int

class FirstUsefulResult(BaseModel):
    time_to_result_s: float
    trials_used: int
    metric_name: str
    metric_value: float

class TrialOut(BaseModel):
    id: int
    experiment_id: int
    params: dict[str, Any]
    metric_name: str
    metric_value: float | None
    early_stopped: bool
    duration_s: float | None
    created_at: datetime

    class Config:
        from_attributes = True

class ExperimentOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    first_useful_result: FirstUsefulResult | None
    task_type: str
    objective_metric: str
    budget_trials: int
    time_limit_minutes: int
    trials: list[TrialOut] = []

    class Config:
        from_attributes = True

class ExperimentStatusOut(BaseModel):
    status: str
    progress_pct: float
    eta_s: float | None
