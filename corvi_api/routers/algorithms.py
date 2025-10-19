from fastapi import APIRouter
router = APIRouter(prefix="/algorithms", tags=["algorithms"])
@router.get("/")
def _list(): return {"ok": True, "resource": "algorithms"}
