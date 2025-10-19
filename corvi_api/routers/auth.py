from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.auth import Token, LoginRequest, RegisterRequest
from security import create_token, verify_password, get_password_hash
from models.user import User, Org, Membership, RoleEnum
from models.subscription import Subscription, SubscriptionTierEnum, UsageQuota

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email==req.email).first():
        raise HTTPException(400, detail="Email already registered")

    try:
        org = Org(name=req.org_name)
        db.add(org)
        db.flush()

        user = User(email=req.email, hashed_password=get_password_hash(req.password), default_org_id=org.id)
        db.add(user)
        db.flush()  # We need it to generate user ID first

        db.add(Membership(user_id=user.id, org_id=org.id, role=RoleEnum.owner))
        db.add(Subscription(org_id=org.id, tier=SubscriptionTierEnum.freemium))
        db.add(UsageQuota(org_id=org.id, key="experiments_per_month", limit=10, used=0))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail="Registration failed. Please try again.")

    access = create_token(str(user.id), 30, "access")
    refresh = create_token(str(user.id), 60*24*7, "refresh")
    return Token(access_token=access, refresh_token=refresh)

@router.post("/token", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")
    access = create_token(str(user.id), 30, "access")
    refresh = create_token(str(user.id), 60*24*7, "refresh")
    return Token(access_token=access, refresh_token=refresh)
