import uuid
from typing import List

from pydantic import BaseModel

from src.api.tdo.order_dto import OrderCreateDto
from src.application.Order.enums import OrderStatus
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.product.enums.enums import ProductSizeEnum
from src.application.product.schemas.product import ProductSchema


class OrderItemSchema(BaseModel):
    id: int = None
    quantity: int
    price: float
    size: ProductSizeEnum
    order_id: int = None
    product_id: uuid.UUID
    product: ProductSchema = None

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int = None
    order_number: str
    status: OrderStatus = OrderStatus.PENDING
    total_price: float

    recipient_name: str
    shipping_address: str
    shipping_city: str
    shipping_postal_code: str
    shipping_country: str
    shipping_method: str

    buyer: BuyerSchema
    order_items: List[OrderItemSchema]



    class Config:
        from_attributes = True




