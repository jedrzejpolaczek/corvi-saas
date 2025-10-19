from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
import enum
from .base import Base

class RoleEnum(enum.IntEnum):
    viewer = 1
    member = 2
    admin = 3
    owner = 4

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    default_org_id = Column(Integer, ForeignKey("orgs.id"), nullable=True)

class Org(Base):
    __tablename__ = "orgs"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Membership(Base):
    __tablename__ = "memberships"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id"), primary_key=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.member)
