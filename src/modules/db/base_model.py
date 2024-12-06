from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.modules.db.database_base import Base as DeclarativeBase

from datetime import datetime, timezone
@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=timezone.utc),
        nullable=False
    )