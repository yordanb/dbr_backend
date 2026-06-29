from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

DATABASE_URL = (
    f"postgresql://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

MTE_DATABASE_URL = (
    f"postgresql://"
    f"{settings.MTE_DB_USER}:"
    f"{settings.MTE_DB_PASSWORD}@"
    f"{settings.MTE_DB_HOST}:"
    f"{settings.MTE_DB_PORT}/"
    f"{settings.MTE_DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

mte_engine = create_engine(
    MTE_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

MteSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=mte_engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mte_db():
    db = MteSessionLocal()
    try:
        yield db
    finally:
        db.close()
