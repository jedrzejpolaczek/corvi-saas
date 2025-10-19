from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    trial_id = Column(Integer, ForeignKey("trials.id"))
    path = Column(String)
    kind = Column(String)
