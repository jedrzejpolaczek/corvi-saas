from sqlalchemy import Column, Integer, String, JSON
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    action = Column(String)
    entity = Column(String)
    entity_id = Column(String)
    details = Column(JSON)
