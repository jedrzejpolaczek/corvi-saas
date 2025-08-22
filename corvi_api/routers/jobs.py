from fastapi import APIRouter
router = APIRouter(prefix="/jobs", tags=["jobs"])
@router.get("/")
def _list(): return {"ok": True, "resource": "jobs"}
