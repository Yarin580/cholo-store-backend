


from fastapi import APIRouter, Depends

from src.api.routes import get_current_admin_user
from src.api.tdo.category_dto import CategoryResponseDto, CategoryCreateDto
from src.api.tdo.order_dto import OrderResponseDto, OrderCreateDto
from src.api.tdo.product_tdo import ProductResponseDto
from src.api.tdo.user_dto import UserResponseDto
from src.application.facades.order_facade import OrderFacade
from src.application.product.services.category import CategoryService

from src.application.product.services.product import ProductService

order_router = APIRouter(prefix="/orders",
                           tags=["orders"])


@order_router.post("/", response_model=OrderResponseDto)
async def create_order(order_to_create: OrderCreateDto):
    return OrderFacade().create_order(order_to_create=order_to_create)