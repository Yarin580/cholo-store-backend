from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.db.base_model import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone