from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create database engine
engine = create_engine(settings.DATABASE_URL)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# FastAPI dependency to provide a database session to routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
