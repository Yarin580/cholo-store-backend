from src.api.tdo.order_dto import OrderCreateDto
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.Order.schemas.order import OrderItemSchema, OrderSchema
from src.application.Order.services.order import OrderService
from src.application.product.services.product import ProductService


class OrderFacade:

    def __init__(self):
        self.order_service = OrderService()
        self.product_service = ProductService()



    def create_order(self, order_to_create: OrderCreateDto):
        buyer_schema = BuyerSchema(name=order_to_create.buyer.name,
                                   email=order_to_create.buyer.email,
                                   phone=order_to_create.buyer.phone)
        print(buyer_schema)

        order_item_schema_list = [OrderItemSchema(product_id=order_item_to_create.product_id,
                                                  quantity=order_item_to_create.quantity,
                                                  price=order_item_to_create.price,
                                                  size=order_item_to_create.size) for order_item_to_create in order_to_create.order_items]
        print(order_item_schema_list)
        order_schema = OrderSchema.from_create_dto(dto=order_to_create)
        print(order_schema)
        order_schema_created = self.order_service.create_order(order=order_schema)
        return order_schema_created






