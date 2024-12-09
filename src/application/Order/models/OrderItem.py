import uuid

from sqlalchemy import Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.application.product.enums.enums import ProductSizeEnum
from src.modules.db.base_model import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    size: Mapped[ProductSizeEnum] = mapped_column(Enum(ProductSizeEnum), nullable=False)

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")

    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    product: Mapped["Product"] = relationship("Product",  lazy="selectin")

    def __init__(self, quantity, price, size, order_id, product_id):
        self.quantity = quantity
        self.price = price
        self.size = size
        self.order_id = order_id
        self.product_id = product_id