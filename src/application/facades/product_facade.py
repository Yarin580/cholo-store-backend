from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tdo.product_size_dto import ProductSizeCreateDto
from src.api.tdo.product_tdo import ProductCreateDto
from src.application.product.models import Product
from src.application.product.repositories.product import ProductRepository
from src.application.product.schemas.product import ProductSchema
from src.application.product.schemas.product_size import ProductSizeSchema
from src.application.product.services.product import ProductService
from src.modules.s3_storage.s3_connection import S3Connection
from config_section.config import config


class ProductFacade:

    def __init__(self, db_session: AsyncSession):
        self.product_service = ProductService(db_session)
        self.s3_storage_service = S3Connection(bucket_name="cholo-store",
                                               access_key=config.AWS_CREDS.aws_access_key_id,
                                               secret_key=config.AWS_CREDS.aws_secret_access_key)



    async def create_new_product(self,
                                 product_dto: ProductCreateDto,
                                 product_image: UploadFile):
        product_sizes_schema = [ProductSizeSchema(**product_size.model_dump()) for product_size in product_dto.product_sizes]
        product_created = await self.product_service.create_new_product(product_data=ProductSchema(**product_dto.model_dump()),
                                                                        product_sizes=product_sizes_schema)

        file_prefix = f"{config.ENV}/collections/{product_created.category_id}/{product_created.id}.jpg"
        self.s3_storage_service.upload_file(file_path=product_image, object_path_key=file_prefix)
        return product_created

