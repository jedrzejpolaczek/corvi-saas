from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.config import settings

Base = declarative_base()

engine = create_engine(settings.DATABASE_URL, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Import models so metadata is ready
from .models import User, Dataset, Experiment, Trial  # noqa: E402,F401

def init_db():
    Base.metadata.create_all(bind=engine)
