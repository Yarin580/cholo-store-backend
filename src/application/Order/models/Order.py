from sqlalchemy import Integer, String, Enum, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.application.Order.enums import OrderStatus
from src.application.Order.models import OrderItem
from src.modules.db.base_model import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Shipping information
    recipient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_address: Mapped[str] = mapped_column(String(1024), nullable=False)
    shipping_city: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_postal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    shipping_country: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_method: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship with Buyer
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("buyers.id"))
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    buyer: Mapped["Buyer"] = relationship("Buyer")

    def __init__(self,
                 order_number: str,
                 status: OrderStatus,
                 total_price: float,
                 recipient_name: str,
                 shipping_address: str,
                 shipping_city: str,
                 shipping_postal_code: str,
                 shipping_country: str,
                 shipping_method: str,
                 buyer_id: int):
        self.order_number = order_number
        self.status = status
        self.total_price = total_price
        self.recipient_name = recipient_name
        self.shipping_address = shipping_address
        self.shipping_city = shipping_city
        self.shipping_postal_code = shipping_postal_code
        self.shipping_country = shipping_country
        self.shipping_method = shipping_method
        self.buyer_id = buyer_id
        self.order_items = []


    def __repr__(self):
        return f"<Order(id={self.id}, order_number={self.order_number}, status={self.status}, total_price={self.total_price}, buyer_id={self.buyer_id})>"

