import uuid

from sqlalchemy.orm import Session

from src.modules.db.base_repository import BaseRepository
from src.application.product.models.product_size import ProductSize
from ..enums.enums import ProductSizeEnum


class ProductSizeRepository(BaseRepository):

    def __init__(self, session: Session = None):
        super().__init__(model=ProductSize, session=session)


    def get_product_size_by_size(self,
                                 product_id: uuid.UUID,
                                 size: ProductSizeEnum) -> ProductSize:
        product_size = self.get(product_id=product_id, size=size.value)
        return None if len(product_size) == 0 else product_size[0]

    def update_product_stock(self,
                             product_id: uuid.UUID,
                             size: ProductSizeEnum,
                             new_stock: int) -> ProductSize:
        with self.get_db_session() as session:
            product_size = session.query(ProductSize).filter_by(product_id=product_id, size=size.value).first()

            product_size.quantity_in_stock = new_stock
            session.flush()
            session.commit()
            return product_size


