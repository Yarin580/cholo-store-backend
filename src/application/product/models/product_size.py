import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.modules.db.base_model import Base

from ..enums.enums import ProductSizeEnum


class ProductSize(Base):
    __tablename__ = "product_sizes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("products.id"), nullable=False)
    size: Mapped[ProductSizeEnum] = mapped_column(Enum(ProductSizeEnum), nullable=False)  # Store size (e.g., 'XS', 'L')
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0)

    product = relationship("Product", back_populates="sizes")  # Establish relationship with Product


    def __init__(self,
                 size: ProductSizeEnum,
                 quantity_in_stock: int,
                 product_id: uuid.UUID) -> None:
        self.size = size
        self.product_id = product_id
        self.quantity_in_stock = quantity_in_stock
