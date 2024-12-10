from sys import exception

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import get_current_admin_user
from src.api.tdo.product_size_dto import ProductSizeCreateDto
from src.api.tdo.product_tdo import ProductResponseDto, ProductCreateDto
from src.application.product.schemas.product import ProductSchema
from src.application.product.schemas.product_size import ProductSizeSchema
from src.application.product.services.product import ProductService
import src.modules.exceptions.base as exceptions
from src.modules.db import get_db_session

product_router = APIRouter(prefix="/products",
                           tags=["products"])


@product_router.get("/",
                    response_model=list[ProductResponseDto])
async def get_all_products(db_session: AsyncSession = Depends(get_db_session)):
    return await ProductService(db_session).get_all_products()


@product_router.get("/{product_id}",
                    response_model=ProductResponseDto)
async def get_product(product_id: str, db_session: AsyncSession = Depends(get_db_session)):
    product = await ProductService(db_session).get_product_by_id(product_id=product_id)
    if not product:
        raise HTTPException(status_code=exceptions.NotFoundException.error_code,
                            detail="product not found")
    return product


@product_router.post("/",
                     response_model=ProductResponseDto, dependencies=[Depends(get_current_admin_user)])
async def create_product(product_dto: ProductCreateDto,
                         product_size: list[ProductSizeCreateDto] = None,
                         db_session: AsyncSession = Depends(get_db_session)):
    product_sizes_schema = [ProductSizeSchema(**product_size.model_dump()) for product_size in product_size]
    return await ProductService(db_session).create_new_product(product_data=ProductSchema(**product_dto.model_dump()),
                                               product_sizes=product_sizes_schema)


