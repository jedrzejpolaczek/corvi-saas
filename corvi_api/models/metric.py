from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    trial_id = Column(Integer, ForeignKey("trials.id"))
    key = Column(String)
    value = Column(Float)
    step = Column(Integer, default=0)
