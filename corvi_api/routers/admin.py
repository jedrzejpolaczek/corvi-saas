from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..security import get_current_user
from ..models.subscription import Subscription, FeatureFlag, UsageQuota, SubscriptionTierEnum

router = APIRouter(prefix="/admin", tags=["admin"]) 

@router.get("/subscriptions")
def list_subs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Subscription).all()

@router.post("/tiers/{org_id}")
def set_tier(org_id: int, tier: SubscriptionTierEnum, db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = db.query(Subscription).filter(Subscription.org_id==org_id).first()
    if not sub:
        sub = Subscription(org_id=org_id, tier=tier)
        db.add(sub)
    else:
        sub.tier = tier
    db.commit()
    return {"ok": True}

@router.post("/feature_flags/{org_id}")
def set_flag(org_id: int, key: str, enabled: bool, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ff = db.query(FeatureFlag).filter(FeatureFlag.org_id==org_id, FeatureFlag.key==key).first()
    if not ff:
        ff = FeatureFlag(org_id=org_id, key=key, enabled=enabled)
        db.add(ff)
    else:
        ff.enabled = enabled
    db.commit()
    return {"ok": True}

@router.post("/quota/{org_id}")
def set_quota(org_id: int, key: str, limit: int, db: Session = Depends(get_db)):
    q = db.query(UsageQuota).filter(UsageQuota.org_id==org_id, UsageQuota.key==key).first()
    if not q:
        q = UsageQuota(org_id=org_id, key=key, limit=limit, used=0)
        db.add(q)
    else:
        q.limit = limit
    db.commit()
    return {"ok": True}
