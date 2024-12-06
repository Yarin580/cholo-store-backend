import uuid

from pydantic import BaseModel

from src.application.product.enums.enums import ProductSizeEnum


class ProductSizeSchema(BaseModel):
    id: int = None
    size: str
    product_id: uuid.UUID = None
    size: ProductSizeEnum
    quantity_in_stock: int

    class Config:
        from_attributes = True
