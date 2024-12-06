import uuid

from pydantic import BaseModel

from src.application.product.schemas.product_size import ProductSizeSchema


class ProductSchema(BaseModel):
    id: uuid.UUID = None
    name: str
    description: str
    original_price: float
    sale_percentage: int = 0
    category_id: int
    sizes: list[ProductSizeSchema] = 'default_factory'

    @property
    def sale_price(self) -> float:
        """Calculate the sale price dynamically."""
        return self.original_price * (1 - self.sale_percentage / 100)

    class Config:
        from_attributes = True
