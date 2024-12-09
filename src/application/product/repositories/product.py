from typing import Union, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import src.modules.exceptions.base as exceptions
from src.modules.db.base_repository import BaseRepository
from src.application.product.models import Product


class ProductRepository(BaseRepository):

    def __init__(self, session: AsyncSession = None):
        super().__init__(model=Product,
                         session=session)


    async def get_by_name(self, name: str) -> Product:
        products = await self.get(name=name)
        return None if len(products) == 0 else products[0]


    async def get_by_category_id(self, category_id: int) -> Union[List[Product], List]:
        products = await self.get(category_id=category_id)
        return [] if len(products) == 0 else products




    
