from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.application.product.models import Category
from src.modules.db.base_repository import BaseRepository


class CategoryRepository(BaseRepository):

    def __init__(self, session: AsyncSession = None):
        super().__init__(model=Category, session=session)


    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.get(id=category_id)
        return None if len(category) == 0 else category[0]

    async def get_category_by_name(self, name: str) -> Category:
        category = await self.get(name=name)
        return None if len(category) == 0 else category[0]