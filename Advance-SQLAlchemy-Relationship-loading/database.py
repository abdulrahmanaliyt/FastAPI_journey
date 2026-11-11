import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session maker
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# Base model class
class Base(DeclarativeBase):
    pass