import uuid
from typing import List

from pydantic import BaseModel

from src.api.tdo.order_dto import OrderCreateDto
from src.application.Order.enums import OrderStatus
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.product.enums.enums import ProductSizeEnum


class OrderItemSchema(BaseModel):
    id: int = None
    quantity: int
    price: float
    size: ProductSizeEnum
    order_id: int = None
    product_id: uuid.UUID

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


    @classmethod
    def from_create_dto(cls, dto: OrderCreateDto) -> "OrderSchema":
        return cls(
            order_number=dto.order_number,
            status=dto.status,
            total_price=dto.total_price,
            recipient_name=dto.recipient_name,
            shipping_address=dto.shipping_address,
            shipping_city=dto.shipping_city,
            shipping_postal_code=dto.shipping_postal_code,
            shipping_country=dto.shipping_country,
            shipping_method=dto.shipping_method,
            buyer = BuyerSchema(name=dto.buyer.name,
                                phone=dto.buyer.phone,
                                email=dto.buyer.email,),
            order_items = dto.order_items
        )


    


    class Config:
        from_attributes = True




