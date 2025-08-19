import io, re, uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.deps import db_session, current_user
from app.schemas.datasets import DatasetOut
from app.models.models import Dataset, User
from app.services.s3 import s3_client
from app.config import settings

router = APIRouter(prefix="/datasets", tags=["datasets"])

SAFE_FILENAME = re.compile(r"[^a-zA-Z0-9._-]")

@router.post("/upload", response_model=DatasetOut)
def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(db_session),
    user: User = Depends(current_user),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv allowed")
    size = 0
    buf = io.BytesIO()
    for chunk in iter(lambda: file.file.read(1024 * 1024), b""):
        size += len(chunk)
        if size > settings.UPLOAD_MAX_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large")
        buf.write(chunk)
    buf.seek(0)
    checksum = s3_client.sha256_of_fileobj(buf)
    safe_name = SAFE_FILENAME.sub("_", file.filename)
    key = f"{user.id}/{uuid.uuid4().hex}_{safe_name}"
    s3_client.upload_fileobj(buf, key, content_type="text/csv")

    ds = Dataset(
        user_id=user.id,
        filename=safe_name,
        size=size,
        checksum=checksum,
        s3_key=key,
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return ds
