from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tdo.order_dto import OrderCreateDto, OrderGetRequestDto
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.Order.schemas.order import OrderItemSchema, OrderSchema
from src.application.Order.services.order import OrderService
from src.application.product.services.product import ProductService


class OrderFacade:

    def __init__(self, db_session: AsyncSession):
        self.order_service = OrderService(db_session)
        self.product_service = ProductService(db_session)



    async def create_order(self, order_to_create: OrderCreateDto):
        buyer_schema = BuyerSchema(name=order_to_create.buyer.name,
                                   email=order_to_create.buyer.email,
                                   phone=order_to_create.buyer.phone)

        order_item_schema_list = [OrderItemSchema(product_id=order_item_to_create.product_id,
                                                  quantity=order_item_to_create.quantity,
                                                  price=order_item_to_create.price,
                                                  size=order_item_to_create.size) for order_item_to_create in order_to_create.order_items]

        order_schema = OrderSchema(order_number=order_to_create.order_number,
                                   total_price=order_to_create.total_price,
                                   recipient_name=order_to_create.recipient_name,
                                   shipping_address=order_to_create.shipping_address,
                                   shipping_city=order_to_create.shipping_city,
                                   shipping_postal_code=order_to_create.shipping_postal_code,
                                   shipping_country=order_to_create.shipping_country,
                                   shipping_method=order_to_create.shipping_method,
                                   buyer = buyer_schema,
                                   order_items=order_item_schema_list)

        order_schema_created = await self.order_service.create_order(order=order_schema)

        return order_schema_created



    async def get_orders(self,
                         order_fields: OrderGetRequestDto):

        return await self.order_service.get_orders(order_number=order_fields.order_number,
                                             buyer_email=order_fields.buyer_email)








