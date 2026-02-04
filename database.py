from asyncio.log import logger
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

db_user = os.getenv("DB_USER", "")    
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "")
db_name = os.getenv("DB_NAME", "")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency that yields a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
