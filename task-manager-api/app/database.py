from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
import os
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Validate database URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
        pool_pre_ping=True,  # Enable connection health checks
        pool_size=5,  # Set connection pool size
        max_overflow=10  # Maximum number of connections to create beyond pool_size
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection established successfully")
except SQLAlchemyError as e:
    logger.error(f"Failed to connect to database: {e}")
    raise

def get_db() -> Generator[Session, None, None]:
    """
    Get database session with automatic cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
