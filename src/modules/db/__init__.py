from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.modules.db.database_base import AsyncSessionLocal
from src.modules.db.session_manager import SessionManager


# Initialize your session factory

async def get_db_session(savepoint: bool = False):
    async with SessionManager(AsyncSessionLocal, savepoint=savepoint) as session:
        yield session
