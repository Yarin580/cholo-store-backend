import uuid

from fastapi import UploadFile, Form
from pydantic import BaseModel, Field
from pydantic.v1 import root_validator

from src.api.tdo.product_size_dto import ProductSizeCreateDto


class ProductResponseDto(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    original_price: float
    sale_price: float
    category_id: int
    sizes: list




class ProductCreateDto(BaseModel):
    name: str
    description: str
    original_price: float
    sale_percentage: int
    category_id: int
    product_sizes: list[ProductSizeCreateDto]