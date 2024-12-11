import json

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes import get_current_admin_user
from src.api.tdo.product_size_dto import ProductSizeCreateDto
from src.api.tdo.product_tdo import ProductResponseDto, ProductCreateDto
from src.application.facades.product_facade import ProductFacade
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
async def create_product(name:str = Form(...),
                         description: str = Form(...),
                         original_price: float = Form(...),
                         sale_percentage: int = Form(0),
                         category_id: int = Form(...),
                         product_sizes: str = Form(...),
                         product_image: UploadFile = File(...),
                         db_session: AsyncSession = Depends(get_db_session)):
    try:
        product_sizes_list = json.loads(product_sizes)  # Convert string to Python list
        product_sizes_objects = [ProductSizeCreateDto(**item) for item in product_sizes_list]

        product_dto = ProductCreateDto(name=name,
                                       description=description,
                                       original_price=original_price,
                                       sale_percentage=sale_percentage,
                                       category_id=category_id,
                                       product_sizes=product_sizes_objects)
        return await ProductFacade(db_session).create_new_product(product_dto=product_dto,
                                                           product_image =product_image)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in product_sizes: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


