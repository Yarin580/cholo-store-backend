import uuid

from pydantic import BaseModel

from src.api.tdo.product_tdo import ProductResponseDto
from src.application.product.enums.enums import ProductSizeEnum


class OrderItemCreateDto(BaseModel):
    price: float
    size: ProductSizeEnum
    quantity: int
    product_id: uuid.UUID


class OrderItemResponseDto(BaseModel):
    id: int
    quantity: int
    product: ProductResponseDto
    price: float
    order_id: int