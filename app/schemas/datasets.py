from pydantic import BaseModel
from datetime import datetime

class DatasetOut(BaseModel):
    id: int
    filename: str
    size: int
    s3_key: str
    created_at: datetime

    class Config:
        from_attributes = True
