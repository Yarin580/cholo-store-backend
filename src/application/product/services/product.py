import uuid
from typing import Optional, List, Union

from src.application.product.enums.enums import ProductSizeEnum
from src.application.product.models import Product, ProductSize
from src.application.product.repositories.category import CategoryRepository
from src.application.product.repositories.product import ProductRepository
import src.modules.exceptions.base as exceptions
from src.application.product.repositories.product_size import ProductSizeRepository
from src.application.product.schemas.product import ProductSchema
from src.application.product.schemas.product_size import ProductSizeSchema



class ProductService:

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()
        self.product_size_repo = ProductSizeRepository()


    def get_all_products(self) -> List[ProductSchema]:
        products =  self.product_repo.get()
        return [ProductSchema.model_validate(product_data) for product_data in products]

    def get_product_by_id(self, product_id: str) -> Optional[ProductSchema]:
        products_res = self.product_repo.get(id=uuid.UUID(product_id))

        return None if len(products_res) == 0 else ProductSchema.model_validate(products_res[0])
    def create_new_product(self,
                           product_data: ProductSchema,
                           product_sizes: list[ProductSizeSchema] = None) -> ProductSchema:

        # check if product already exist
        product = self.product_repo.get_by_name(name=product_data.name)
        if product:
            raise exceptions.DuplicateValueException(message=f"Product {product_data.name} already exists")

        # check if there is a category
        product_category = self.category_repo.get_category_by_id(category_id=product_data.category_id)
        if not product_category:
            raise exceptions.NotFoundException("Category not found")

        product = Product(**product_data.model_dump(exclude_defaults=True))
        product_created = ProductSchema.model_validate(self.product_repo.create(product))
        if product_sizes:
            for product_size in product_sizes:
                product_size.product_id = product_created.id
                product_size = ProductSize(**product_size.model_dump(exclude_defaults=True))
                product_created.sizes.append(ProductSizeSchema.model_validate(self.product_size_repo.create(product_size)))


        return product_created


    def get_products_by_category(self, category_id: int) -> List[ProductSchema]:

        #check if category exist
        category = self.category_repo.get_category_by_id(category_id=category_id)
        if not category:
            raise exceptions.NotFoundException("Category not found")

        products = self.product_repo.get_by_category_id(category_id=category_id)
        return [ProductSchema.model_validate(product_data) for product_data in products]



