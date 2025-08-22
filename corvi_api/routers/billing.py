from fastapi import APIRouter
router = APIRouter(prefix="/billing", tags=["billing"])
@router.get("/")
def _list(): return {"ok": True, "resource": "billing"}
