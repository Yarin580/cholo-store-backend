import uuid

from pydantic import BaseModel, Field
from pydantic.v1 import root_validator


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
    sale_percentage: int = 0
    category_id: int