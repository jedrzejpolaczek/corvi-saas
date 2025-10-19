from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    name = Column(String)
    key = Column(String, unique=True)
