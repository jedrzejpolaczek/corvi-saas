from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    path = Column(String)
    rows = Column(Integer)
    cols = Column(Integer)
    target = Column(String, nullable=True)
    format = Column(String)
