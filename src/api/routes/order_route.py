from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import get_current_admin_user
from src.api.tdo.category_dto import CategoryResponseDto, CategoryCreateDto
from src.api.tdo.order_dto import OrderResponseDto, OrderCreateDto, OrderGetRequestDto
from src.api.tdo.product_tdo import ProductResponseDto
from src.api.tdo.user_dto import UserResponseDto
from src.application.facades.order_facade import OrderFacade
from src.application.product.services.category import CategoryService

from src.application.product.services.product import ProductService
from src.modules.db import get_db_session

order_router = APIRouter(prefix="/orders",
                           tags=["orders"])


@order_router.get("/", response_model=List[OrderResponseDto])
async def get_orders(filters: OrderGetRequestDto = Depends(),
                     db_session: AsyncSession = Depends(get_db_session)):
    return await OrderFacade(db_session).get_orders(filters)

@order_router.post("/", response_model=OrderResponseDto)
async def create_order(order_to_create: OrderCreateDto,
                       db_session: AsyncSession = Depends(get_db_session)):
    return await OrderFacade(db_session).create_order(order_to_create=order_to_create)