import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.modules.db.base_repository import BaseRepository
from src.application.product.models.product_size import ProductSize
from ..enums.enums import ProductSizeEnum


class ProductSizeRepository(BaseRepository):

    def __init__(self, session: AsyncSession = None):
        super().__init__(model=ProductSize, session=session)


    async def get_product_size_by_size(self,
                                 product_id: uuid.UUID,
                                 size: ProductSizeEnum) -> ProductSize:
        product_size = await self.get(product_id=product_id, size=size.value)
        return None if len(product_size) == 0 else product_size[0]

    async def update_product_stock(self,
                             product_id: uuid.UUID,
                             size: ProductSizeEnum,
                             new_stock: int) -> ProductSize:

            product_size = await self.get(product_id=product_id, size=size.value)
            product_size = product_size[0]
            product_size.quantity_in_stock = new_stock

            updated_product_size = await self.update(product_size)
            return updated_product_size


