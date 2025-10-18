from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user
from models.roi import ROIFormula
from feature_gating import enforce_feature, Feature

router = APIRouter(prefix="/projects", tags=["roi"]) 

@router.put("/{id}/roi_formula", dependencies=[Depends(enforce_feature(Feature.KPI_ROI))])
def put_formula(id: int, formula: str, baseline: float, business_factor: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.query(ROIFormula).filter(ROIFormula.project_id==id).first()
    if not row:
        row = ROIFormula(project_id=id)
        db.add(row)
    row.formula = formula
    row.baseline = baseline
    row.business_factor = business_factor
    db.commit()
    return {"ok": True}

@router.get("/{id}/roi_report", dependencies=[Depends(enforce_feature(Feature.KPI_ROI))])
def get_report(id: int, metric: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.query(ROIFormula).filter(ROIFormula.project_id==id).first()
    if not row:
        row = ROIFormula(project_id=id)
        db.add(row)
        db.commit()
    result = (metric - row.baseline) * row.business_factor
    return {"formula": row.formula, "result": result}
