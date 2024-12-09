from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Query, Session, selectinload
from typing import List, Type, TypeVar, Optional, Dict, Any
from src.modules.db.base_model import Base
from .session_manager import SessionManager
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self._session = session


    async def get(self,relationships: list = None, **filters ) -> list[ModelType]:
        model_query = select(self.model)
        if filters:
            for attr, value in filters.items():
                model_query = model_query.filter(getattr(self.model, attr) == value)

        if relationships:
            for relationship in relationships:
                if hasattr(self.model, relationship):
                    model_query = model_query.options(selectinload(getattr(self.model, relationship)))

        result = await self._session.execute(model_query)
        records = result.scalars().all()
        return records if records else []


    async def create(self, obj_data: ModelType) -> ModelType:
        self._session.add(obj_data)
        await self._session.flush()
        return obj_data

    async def delete(self, obj_id: int) -> bool:

        db_obj = await self.get(id=obj_id)
        if not db_obj:
            return False
        await self._session.delete(db_obj)
        await self._session.flush()
        return True


    async def update(self, obj_data: ModelType) -> ModelType:
        self._session.add(obj_data)
        await self._session.refresh(obj_data)
        return obj_data

