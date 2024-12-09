

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import get_current_admin_user
from src.api.tdo.category_dto import CategoryResponseDto, CategoryCreateDto
from src.api.tdo.product_tdo import ProductResponseDto
from src.api.tdo.user_dto import UserResponseDto
from src.application.product.services.category import CategoryService

from src.application.product.services.product import ProductService
from src.modules.db import get_db_session

category_route = APIRouter(prefix="/categories",
                           tags=["categories"])


@category_route.get("/", response_model=list[CategoryResponseDto])
async def get_categories(category_id: int = None,
                         category_name: str = None,
                         db_session: AsyncSession = Depends(get_db_session)):
    return await CategoryService(db_session).get_categories(category_id=category_id, category_name=category_name)

@category_route.get("/{category_id}", response_model=CategoryResponseDto)
async def get_category(category_id: int,
                       db_session: AsyncSession = Depends(get_db_session)):
    return await CategoryService(db_session).get_category_by_id(category_id=category_id)


@category_route.get("/{category_id}/products",
                    response_model=list[ProductResponseDto])
async def get_products_by_categories(category_id: int,
                                     db_session: AsyncSession = Depends(get_db_session)):
    return await ProductService(db_session).get_products_by_category(category_id=category_id)

@category_route.post("/", response_model=CategoryResponseDto)
async def create_category(category_to_create: CategoryCreateDto,
                          db_session: AsyncSession = Depends(get_db_session),
                          admin_user: UserResponseDto = Depends(get_current_admin_user)):
    return CategoryService(db_session).create_category(category_dto=category_to_create)




