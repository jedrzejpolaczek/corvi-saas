from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from security import get_current_user
from models.subscription import Subscription, FeatureFlag, UsageQuota

router = APIRouter(prefix="/features", tags=["features"]) 

@router.get("/")
def get_features(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sub = db.query(Subscription).filter(Subscription.org_id==user.default_org_id).first()
    flags = db.query(FeatureFlag).filter(FeatureFlag.org_id==user.default_org_id).all()
    quotas = db.query(UsageQuota).filter(UsageQuota.org_id==user.default_org_id).all()
    return {
        "tier": sub.tier.value if sub else "freemium",
        "flags": {f.key: f.enabled for f in flags},
        "quotas": {q.key: {"limit": q.limit, "used": q.used} for q in quotas},
    }
