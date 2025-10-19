from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from .base import Base

class Trial(Base):
    __tablename__ = "trials"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    params = Column(JSON)
    status = Column(String, default="queued")
    value = Column(String, nullable=True)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    kind = Column(String)
    payload = Column(JSON)
    status = Column(String, default="queued")
    attempts = Column(Integer, default=0)
