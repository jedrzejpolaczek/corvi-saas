from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd, io
from ..db import get_db
from ..security import get_current_user
from ..models.dataset import Dataset
from ..s3 import put_object

router = APIRouter(prefix="/datasets", tags=["datasets"]) 

@router.post("/upload")
async def upload_dataset(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    content = await file.read()
    if len(content) > 200 * 1024 * 1024:
        raise HTTPException(400, detail="File too large (200MB limit in demo)")
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
            fmt = "csv"
        elif file.filename.endswith(".parquet"):
            df = pd.read_parquet(io.BytesIO(content))
            fmt = "parquet"
        else:
            raise HTTPException(400, detail="Unsupported format")
    except Exception as e:
        raise HTTPException(400, detail=f"Parse error: {e}")
    key = f"org-{user.default_org_id}/proj-{project_id}/datasets/{file.filename}"
    path = f"s3://corvi/{key}"
    try:
        put_object(key, content, file.content_type or "application/octet-stream")
    except Exception:
        # Fallback for CI/local without MinIO
        path = f"file://{file.filename}"
    ds = Dataset(project_id=project_id, path=path, rows=df.shape[0], cols=df.shape[1], format=fmt)
    db.add(ds); db.commit()
    preview = df.head(20).to_dict(orient="records")
    issues = []
    if df.isna().any().any():
        issues.append("Missing values detected")
    return {"id": ds.id, "rows": ds.rows, "cols": ds.cols, "preview": preview, "issues": issues}
