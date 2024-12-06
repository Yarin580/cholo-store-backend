from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config_section.config import config

DATABASE_URL = config.DB_URL

engine = create_engine(url=DATABASE_URL, echo=False, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
)