from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, Float,
    ForeignKey, Index
)
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
try:
    from sqlalchemy.dialects.postgresql import JSONB
    JSONType = JSONB
except Exception:
    JSONType = SQLITE_JSON
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    datasets = relationship("Dataset", back_populates="user")
    experiments = relationship("Experiment", back_populates="user")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(512), nullable=False)
    size = Column(Integer, nullable=False)
    checksum = Column(String(128), nullable=False)
    s3_key = Column(String(1024), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="datasets")

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    task_type = Column(String(64), nullable=False)  # "classification" | "regression"
    objective_metric = Column(String(64), nullable=False)  # "accuracy" | "r2"
    budget_trials = Column(Integer, nullable=False)
    time_limit_minutes = Column(Integer, nullable=False)

    status = Column(String(32), default="queued", nullable=False)  # queued|running|finished|stopped|failed
    stop_requested = Column(Boolean, default=False, nullable=False)

    # First useful result snapshot
    first_result_time_s = Column(Float, nullable=True)
    first_result_trials_used = Column(Integer, nullable=True)
    first_result_metric_name = Column(String(64), nullable=True)
    first_result_metric_value = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="experiments")
    dataset = relationship("Dataset")
    trials = relationship("Trial", back_populates="experiment", cascade="all, delete-orphan")

Index("ix_experiments_user_created", Experiment.user_id, Experiment.created_at)

class Trial(Base):
    __tablename__ = "trials"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), index=True, nullable=False)
    params = Column(JSONType, nullable=False)
    metric_name = Column(String(64), nullable=False)
    metric_value = Column(Float, nullable=True)
    early_stopped = Column(Boolean, default=False, nullable=False)
    duration_s = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    experiment = relationship("Experiment", back_populates="trials")
