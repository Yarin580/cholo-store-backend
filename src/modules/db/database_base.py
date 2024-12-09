from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .session_manager import SessionManager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config_section.config import config
DATABASE_URL = config.DB_URL

engine = create_async_engine(url=DATABASE_URL, echo=False)

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


session_manager = SessionManager(AsyncSessionLocal)