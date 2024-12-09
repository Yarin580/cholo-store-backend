from typing import List, Optional

from pydantic import BaseModel

from src.api.tdo.buyer_dto import BuyerCreateDto, BuyerResponseDto
from src.api.tdo.order_item import OrderItemCreateDto, OrderItemResponseDto
from src.application.Order.enums import OrderStatus
from src.application.Order.models import Buyer


class OrderBaseDto(BaseModel):
    total_price: float
    recipient_name: str
    shipping_address: str
    shipping_city: str
    shipping_postal_code: str
    shipping_country: str
    shipping_method: str
    order_number: str

class OrderCreateDto(OrderBaseDto):
    order_items: List[OrderItemCreateDto]
    buyer: BuyerCreateDto

class OrderResponseDto(OrderBaseDto):
    id: int
    status: OrderStatus
    order_items: List[OrderItemResponseDto] = 'default_factory'
    buyer: BuyerResponseDto = None

class OrderGetRequestDto(BaseModel):
    order_number: Optional[str] = None
    buyer_email: Optional[str] = None