from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable - use persistent storage
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./content_agent.db")
if "postgres" in DATABASE_URL or "postgresql" in DATABASE_URL:
    DATABASE_URL = "sqlite:///./content_agent.db"

# Use persistent storage location for cloud deployment
if DATABASE_URL.startswith("sqlite"):
    # Use /tmp directory which persists longer on Render
    DATABASE_URL = "sqlite:////tmp/content_agent.db"
    print(f"Using persistent database: {DATABASE_URL}")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
