from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tdo.category_dto import CategoryCreateDto
from src.application.product.models import Category
from src.application.product.repositories.category import CategoryRepository
from src.application.product.repositories.product import ProductRepository
from src.application.product.schemas.category import CategorySchema
import src.modules.exceptions.base as exceptions
from src.modules.db.database_base import session_manager
from src.utils import remove_non_args


class CategoryService:

    def __init__(self, db_session: AsyncSession):
        self.category_repository = CategoryRepository(db_session)
        self.product_repository = ProductRepository(db_session)

    async def get_categories(self,
                       category_id: int,
                       category_name: str) -> list[CategorySchema]:

        filters = remove_non_args(id = category_id,
                                  name = category_name)


        categories = await self.category_repository.get(**filters)
        return [CategorySchema.model_validate(category_data) for category_data in categories]


    async def get_category_by_id(self, category_id: int) -> CategorySchema:

        category = await self.category_repository.get_category_by_id(category_id=category_id)
        if not category:
            raise exceptions.NotFoundException("there is now category matching id {}".format(category_id))

        return CategorySchema.model_validate(category)

    async def create_category(self, category_dto: CategoryCreateDto) -> CategorySchema:
        category = await self.category_repository.get_category_by_name(name=category_dto.name)
        if category:
            raise exceptions.DuplicateValueException("category name {} already exists".format(category_dto.name))

        try:
            category_to_create = Category(name=category_dto.name)
            category_created = await self.category_repository.create(obj_data=category_to_create)
            return CategorySchema.model_validate(category_created)
        except Exception as e:
            raise Exception("Error creating category {}: {}".format(category_dto.name, e))

