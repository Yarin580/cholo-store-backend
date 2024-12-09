from sqlalchemy.ext.asyncio import AsyncSession

from src.application.Order.models import OrderItem
from src.modules.db.base_repository import BaseRepository


class OrderItemRepository(BaseRepository):

    def __init__(self, session: AsyncSession = None):
        super().__init__(session=session, model=OrderItem)