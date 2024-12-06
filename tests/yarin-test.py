# from src.application.product.enums.enums import ProductSizeEnum
# from src.application.product.repositories.product import ProductRepository
# from src.application.product.repositories.product_size import ProductSizeRepository
# from src.application.product.schemas.product import ProductSchema
# from src.application.product.services.product import ProductService
#
# product_repository = ProductRepository()
# # print(product_repository.get_by_name(name="t-shirt"))
#
# product = ProductSchema(name="just_Check", description="Just Check", original_price=200, sale_percentage=30, category_id=1)
# product_service = ProductService()
# product_service.create_new_product(product_data=product)
#
# #
# # product = {
# #     "name" : "t-shirt", "description" : "חולצה", "original_price" : "100", "sale_percentage" : "10",
# # "category_id" : 1
# # }
# #
# # # product_repository.create(product)
# # #
# # # from src.modules.db.base_model import Base
# # # from src.modules.db.database_base import engine
# # #
# # # Base.metadata.create_all(bind=engine)
# #
# # # print(product_repository.get_by_name(name="t-sdhirt"))
# #
# # product_size_repo = ProductSizeRepository()
# # product_size = {"product_id": 1, "size": ProductSizeEnum.XL, "quantity_in_stock": 2}
# #
# # # product_size_repo.create(obj_data=product_size)
# #
# # print(product_size_repo.update_product_stock(product_id=1, size=ProductSizeEnum.XL, new_stock=10))
#
#
#
# # product_service = ProductService()
# #
# # print(product_service.create_new_product(name="new tshirt",
# #                                          description="yairn yarin",
# #                                          category_id=1,
# #                                          original_price=100))
from src.api.tdo.buyer_dto import BuyerCreateDto
from src.api.tdo.order_dto import OrderCreateDto
from src.api.tdo.order_item import OrderItemCreateDto
from src.application.Order.enums import OrderStatus
from src.application.facades.order_facade import OrderFacade
from src.application.product.enums.enums import ProductSizeEnum

order_create_dto_invalid = OrderCreateDto(
    total_price=150.0,
    status=OrderStatus.PENDING,
    recipient_name="Invalid User",
    shipping_address="",
    shipping_city="Invalid City",
    shipping_postal_code="",
    shipping_country="",
    shipping_method="Invalid",
    order_number="ORD123469",
    order_items=[
        OrderItemCreateDto(
            price=100.0,
            size=ProductSizeEnum.XL,
            quantity=1,
            product_id="1ecb549c-ebc6-45cd-9fff-0b074d971254"
        ),
        OrderItemCreateDto(
            price=50.0,
            size=ProductSizeEnum.XL,
            quantity=3,
            product_id="050fb38d-c0e0-459a-b7f5-050aa91e0853"
        )
    ],
    buyer=BuyerCreateDto(
        name="Invalid User",
        email="",  # Missing email
        phone="123-456-7890"
    )
)




print(OrderFacade().create_order(order_to_create=order_create_dto_invalid))