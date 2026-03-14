"""
Database Configuration
SQLAlchemy engine, session, and Base for the AI Legal Assistant.
Uses SQLite for development; swap to PostgreSQL via DATABASE_URL env var.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use DATABASE_URL env var for production (PostgreSQL on Render)
# Falls back to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or DATABASE_URL.strip() == "":
    DATABASE_URL = "sqlite:///./legal_assistant.db"
    print("ℹ️ Using SQLite database (local)")
else:
    # SQLAlchemy 2.0+ requires postgresql:// not postgres://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Mask password for logging
    masked_url = DATABASE_URL
    if "@" in DATABASE_URL:
        protocol, rest = DATABASE_URL.split("://", 1)
        auth, host_path = rest.split("@", 1)
        masked_url = f"{protocol}://****@{host_path}"
    print(f"✅ Using database: {masked_url}")

# SQLite needs check_same_thread=False for FastAPI async
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
except Exception as e:
    print(f"❌ Failed to create database engine: {e}")
    raise
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called on application startup."""
    try:
        from sqlalchemy.exc import OperationalError
        Base.metadata.create_all(bind=engine)
        print("🏛️ Database tables verified/created")
    except OperationalError as e:
        if "already exists" in str(e).lower():
            print("🏛️ Tables already exist, skipping DDL")
        else:
            print(f"❌ Database error: {e}")
            raise
    except Exception as e:
        print(f"❌ Unexpected database initialization error: {e}")
        raise
