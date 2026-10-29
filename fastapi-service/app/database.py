import os

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},)

SessionLocal = sessionmaker(bind=engine, autoflush=False,)

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db