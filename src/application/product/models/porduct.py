from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import mapped_column

from src.modules.db.base_model import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID]= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)
    original_price: Mapped[float] = mapped_column(Float)
    sale_percentage: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products", lazy="selectin")
    sizes = relationship("ProductSize", back_populates="product", lazy="selectin")

    def __init__(self,
                 name: str,
                 description: str,
                 original_price: float,
                 category_id: int,
                 sale_percentage: int = 0,
                 **kw: Any):
        super().__init__(**kw)
        self.name = name.lower()
        self.description = description
        self.original_price = original_price
        self.sale_percentage = sale_percentage
        self.category_id = category_id
