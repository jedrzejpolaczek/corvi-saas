from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
import io, csv
import pandas as pd
from ..db import get_db
from ..security import get_current_user
from ..models.job import Trial
from ..feature_gating import enforce_feature, Feature

router = APIRouter(prefix="/exports", tags=["exports"]) 

@router.get("/experiments/{id}.csv", dependencies=[Depends(enforce_feature(Feature.EXPORTS))])
def export_csv(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    trials = db.query(Trial).filter(Trial.experiment_id==id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["trial_id","params","value","status"]) 
    for t in trials:
        writer.writerow([t.id, t.params, t.value, t.status])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")

@router.get("/experiments/{id}.parquet", dependencies=[Depends(enforce_feature(Feature.EXPORTS))])
def export_parquet(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    trials = db.query(Trial).filter(Trial.experiment_id==id).all()
    df = pd.DataFrame([{"trial_id": t.id, "params": t.params, "value": t.value, "status": t.status} for t in trials])
    buf = io.BytesIO(); df.to_parquet(buf); buf.seek(0)
    return StreamingResponse(iter([buf.getvalue()]), media_type="application/octet-stream")

@router.get("/experiments/{id}.pdf", dependencies=[Depends(enforce_feature(Feature.EXPORTS))])
def export_pdf(id: int):
    return JSONResponse({"url": f"/dashboard/exports/experiments/{id}.pdf"})
