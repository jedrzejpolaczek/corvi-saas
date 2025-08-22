from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class ROIFormula(Base):
    __tablename__ = "roi_formulas"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    formula = Column(String, default="(metric - baseline) * business_factor")
    baseline = Column(Float, default=0.0)
    business_factor = Column(Float, default=1.0)
