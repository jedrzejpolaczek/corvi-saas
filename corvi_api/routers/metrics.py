from fastapi import APIRouter
router = APIRouter(prefix="/metrics", tags=["metrics"])
@router.get("/")
def _list(): return {"ok": True, "resource": "metrics"}
