from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .security import get_current_user
from .models.subscription import SubscriptionTierEnum, FeatureFlag, Subscription

class Feature:
    CORVI_OPT = "corvi_opt"
    KPI_ROI = "kpi_roi"
    EXPORTS = "exports"
    MULTI_PROJECT = "multi_project"
    BI_DASHBOARD = "bi_dashboard"

def enforce_feature(feature_key: str):
    def _checker(db: Session = Depends(get_db), user=Depends(get_current_user)):
        sub = db.query(Subscription).filter(Subscription.org_id==user.default_org_id).first()
        if not sub:
            raise HTTPException(status_code=402, detail="No subscription")
        if sub.tier == SubscriptionTierEnum.freemium:
            if feature_key in [Feature.CORVI_OPT, Feature.KPI_ROI, Feature.BI_DASHBOARD, Feature.MULTI_PROJECT, Feature.EXPORTS]:
                raise HTTPException(status_code=402, detail="Feature requires Premium")
        ff = db.query(FeatureFlag).filter(FeatureFlag.org_id==user.default_org_id, FeatureFlag.key==feature_key).first()
        if ff and not ff.enabled:
            raise HTTPException(status_code=402, detail="Feature disabled by admin")
        return True
    return _checker

def enforce_quota(quota_key: str):
    from .models.subscription import UsageQuota
    def _checker(db: Session = Depends(get_db), user=Depends(get_current_user)):
        q = db.query(UsageQuota).filter(UsageQuota.org_id==user.default_org_id, UsageQuota.key==quota_key).first()
        if q and q.used >= q.limit:
            raise HTTPException(status_code=429, detail=f"Quota exceeded: {quota_key}")
        return True
    return _checker
