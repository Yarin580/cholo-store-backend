from pydantic import BaseModel

from src.application.product.enums.enums import ProductSizeEnum


class ProductSizeCreateDto(BaseModel):
    size: ProductSizeEnum
    quantity_in_stock: int