from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from src.application.user.enums import UserRoles
from src.modules.db.base_model import Base

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)

    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles),index=True)

    def __init__(self,
                 username: str,
                 hashed_password: str,
                 email: str,
                 role: UserRoles):
        super().__init__()
        self.username = username
        self.hashed_password=hashed_password
        self.email=email
        self.role=role