from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import get_settings

settings = get_settings()

DB_URL = settings.DB_URL

engine = create_engine(DB_URL, pool_pre_ping=True)

session_local = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    except Exception as e:
        print(e)


