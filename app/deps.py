from fastapi import Depends
from sqlalchemy.orm import Session
from app.security import get_db, get_current_user
from app.models.models import User

def db_session() -> Session:
    yield from get_db()

def current_user(user: User = Depends(get_current_user)) -> User:
    return user
