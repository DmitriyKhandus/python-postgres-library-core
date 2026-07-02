import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def build_database_url() -> str:
    db_user = os.getenv("DB_USER", "octagon")
    db_password = os.getenv("DB_PASSWORD", "12345")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "octagon_db")

    return (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


Base = declarative_base()

engine = create_engine(
    build_database_url(),
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def create_tables() -> None:
    from app.db import models

    Base.metadata.create_all(bind=engine)
