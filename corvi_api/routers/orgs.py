from fastapi import APIRouter
router = APIRouter(prefix="/orgs", tags=["orgs"])
@router.get("/")
def _list(): return {"ok": True, "resource": "orgs"}
