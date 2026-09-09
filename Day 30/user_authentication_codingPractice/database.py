from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

# Get the project folder
BASE_DIR = Path(__file__).resolve().parent

# Store database inside the project folder
DATABASE_PATH = BASE_DIR / "users.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ============================================================
# DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# ============================================================
# BASE CLASS
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    Create a database session for each request.
    Close the session after the request is completed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()