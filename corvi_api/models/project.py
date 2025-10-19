from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    name = Column(String)
