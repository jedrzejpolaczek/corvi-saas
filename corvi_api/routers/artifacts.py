from fastapi import APIRouter
router = APIRouter(prefix="/artifacts", tags=["artifacts"])
@router.get("/")
def _list(): return {"ok": True, "resource": "artifacts"}
