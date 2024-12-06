from src.api.tdo.category_dto import CategoryCreateDto
from src.application.product.models import Category
from src.application.product.repositories.category import CategoryRepository
from src.application.product.schemas.category import CategorySchema
import src.modules.exceptions.base as exceptions
from src.utils import remove_non_args


class CategoryService:

    def __init__(self):
        self.category_repository = CategoryRepository()

    def get_categories(self,
                       category_id: int,
                       category_name: str) -> list[CategorySchema]:

        filters = remove_non_args(id = category_id,
                                  name = category_name)

        categories = self.category_repository.get(**filters)
        print(categories)
        return [CategorySchema.model_validate(category_data) for category_data in categories]


    def get_category_by_id(self, category_id: int) -> CategorySchema:

        category = self.category_repository.get_category_by_id(category_id=category_id)
        if not category:
            raise exceptions.NotFoundException("there is now category matching id {}".format(category_id))

        return CategorySchema.model_validate(category)

    def create_category(self, category_dto: CategoryCreateDto) -> CategorySchema:
        category = self.category_repository.get_category_by_name(name=category_dto.name)
        if category:
            raise exceptions.DuplicateValueException("category name {} already exists".format(category_dto.name))

        try:
            category_to_create = Category(name=category_dto.name)
            category_created = self.category_repository.create(obj_data=category_to_create)
            return CategorySchema.model_validate(category_created)
        except Exception as e:
            raise Exception("Error creating category {}: {}".format(category_dto.name, e))

