from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
import enum
from .base import Base

class SubscriptionTierEnum(str, enum.Enum):
    freemium = "freemium"
    premium_basic = "premium_basic"
    premium_pro = "premium_pro"
    enterprise = "enterprise"

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"), unique=True)
    tier = Column(Enum(SubscriptionTierEnum), default=SubscriptionTierEnum.freemium)

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    key = Column(String)
    enabled = Column(Boolean, default=True)

class UsageQuota(Base):
    __tablename__ = "usage_quotas"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"))
    key = Column(String)
    limit = Column(Integer)
    used = Column(Integer, default=0)
