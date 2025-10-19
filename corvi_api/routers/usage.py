from fastapi import APIRouter
router = APIRouter(prefix="/usage", tags=["usage"])
@router.get("/")
def _list(): return {"ok": True, "resource": "usage"}
