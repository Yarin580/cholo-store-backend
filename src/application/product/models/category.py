from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from src.modules.db.base_model import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    products = relationship("Product", back_populates="category")

    def __init__(self,
                 name: str):
        super().__init__()
        self.name = name