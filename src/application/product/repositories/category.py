from typing import Union

from sqlalchemy.orm import Session

from src.application.product.models import Category
from src.modules.db.base_repository import BaseRepository


class CategoryRepository(BaseRepository):

    def __init__(self, session: Session = None):
        super().__init__(model=Category, session=session)


    def get_category_by_id(self, category_id: int) -> Category:
        category = self.get(id=category_id)
        return None if len(category) == 0 else category[0]

    def get_category_by_name(self, name: str) -> Category:
        category = self.get(name=name)
        return None if len(category) == 0 else category[0]