from fastapi import APIRouter
router = APIRouter(prefix="/users", tags=["users"])
@router.get("/")
def _list(): return {"ok": True, "resource": "users"}
