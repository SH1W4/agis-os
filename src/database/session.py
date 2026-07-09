"""
Database session management for LogisticSmart v3.0
Supports both SQLite (development) and PostgreSQL (production)
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, NullPool
from contextlib import contextmanager
import logging

from .models import Base
from src.config.settings import settings

logger = logging.getLogger(__name__)

# Database configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Use settings.DATABASE_URL if available, otherwise fallback to SQLite
DATABASE_URL = settings.DATABASE_URL if hasattr(settings, 'DATABASE_URL') else os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_DIR}/logistic_smart.db"
)

# Create engine with appropriate settings based on database type
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DATABASE_ECHO
    )
elif "postgresql" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DATABASE_ECHO
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=settings.DATABASE_ECHO
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def get_db() -> Session:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()
