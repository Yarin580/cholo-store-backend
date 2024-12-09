import asyncio
import uuid
from typing import Optional, List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.product.enums.enums import ProductSizeEnum
from src.application.product.models import Product, ProductSize
from src.application.product.repositories.category import CategoryRepository
from src.application.product.repositories.product import ProductRepository
import src.modules.exceptions.base as exceptions
from src.application.product.repositories.product_size import ProductSizeRepository
from src.application.product.schemas.product import ProductSchema
from src.application.product.schemas.product_size import ProductSizeSchema

from src.modules.db.database_base import session_manager


class ProductService:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.product_repository = ProductRepository(db_session)
        self.product_size_repository = ProductSizeRepository(db_session)
        self.category_repository = CategoryRepository(db_session)


    async def get_all_products(self) -> List[ProductSchema]:
        products =  await self.product_repository.get()
        return [ProductSchema.model_validate(product_data) for product_data in products]

    async def get_product_by_id(self, product_id: str) -> Optional[ProductSchema]:
        products_res = await self.product_repository.get(id=uuid.UUID(product_id))
        return None if len(products_res) == 0 else ProductSchema.model_validate(products_res[0])


    async def create_new_product(self,
                           product_data: ProductSchema,
                           product_sizes: list[ProductSizeSchema] = None) -> ProductSchema:
        product = await self.product_repository.get_by_name(name=product_data.name)
        if product:
            raise exceptions.DuplicateValueException(message=f"Product {product_data.name} already exists")

        #check if there is a category
        product_category = self.category_repository.get_category_by_id(category_id=product_data.category_id)
        if not product_category:
            raise exceptions.NotFoundException("Category not found")

        product = Product(**product_data.model_dump(exclude_defaults=True))
        product_created = await self.product_repository.create(product)
        product_created = (await self.product_repository.get(id=product_created.id))[0]


        product_created = ProductSchema.model_validate(product_created)
        if product_sizes:
            for product_size in product_sizes:
                product_size.product_id = product_created.id
                product_size = ProductSize(**product_size.model_dump(exclude_defaults=True))
                product_created.sizes.append(ProductSizeSchema.model_validate(await self.product_size_repository.create(product_size)))


        return product_created


    async def get_products_by_category(self, category_id: int) -> List[ProductSchema]:

        #check if category exist
        category = await self.category_repository.get_category_by_id(category_id=category_id)
        if not category:
            raise exceptions.NotFoundException("Category not found")

        products = await self.product_repository.get(category_id=category.id)
        return [ProductSchema.model_validate(product_data) for product_data in products]



#
# product_to_create = ProductSchema(name="Product2",
#                                   description="Product description",
#                                   original_price=2,
#                                   sale_percentage=0,
#                                   category_id=1,
#                                   )
#
# product_size_to_create = [
#     ProductSizeSchema(size=ProductSizeEnum.XL,
#                       quantity_in_stock=5)
# ]
#
# asyncio.run(ProductService().create_new_product(product_to_create, product_size_to_create))
