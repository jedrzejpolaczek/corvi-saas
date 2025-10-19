from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum
import enum
from .base import Base

class AlgoEnum(str, enum.Enum):
    grid = "grid"
    random = "random"
    corvi_opt = "corvi_opt"

class BackendEnum(str, enum.Enum):
    local = "local"
    ray = "ray"

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    algorithm = Column(Enum(AlgoEnum))
    backend = Column(Enum(BackendEnum), default=BackendEnum.local)
    space = Column(JSON)
    status = Column(String, default="created")
    best_metric = Column(String, nullable=True)
    best_value = Column(String, nullable=True)
