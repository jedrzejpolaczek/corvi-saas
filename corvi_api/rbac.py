from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.user import Membership, RoleEnum
from security import get_current_user

def require_role(min_role: RoleEnum):
    def _checker(org_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
        m = db.query(Membership).filter(Membership.org_id==org_id, Membership.user_id==user.id).first()
        if not m:
            raise HTTPException(status_code=403, detail="No org membership")
        if m.role.value < min_role.value:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return True
    return _checker
