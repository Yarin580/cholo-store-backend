import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.tdo import order_item
from src.application.Order.enums import OrderStatus
from src.application.Order.models import OrderItem, Buyer, Order
from src.application.Order.repositories.Buyer import BuyerRepository
from src.application.Order.repositories.Order import OrderRepository
from src.application.Order.repositories.OrderItem import OrderItemRepository
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.Order.schemas.order import OrderSchema, OrderItemSchema
from src.application.product.repositories.product import ProductRepository
from src.application.product.repositories.product_size import ProductSizeRepository
from src.application.product.schemas.product import ProductSchema
from src.application.product.services.product import ProductService

import src.modules.exceptions.base as exceptions
from src.modules.db.database_base import session_manager
from src.utils import remove_non_args


class OrderService:

    def __init__(self, db_session: AsyncSession):
        self.order_repository = OrderRepository(db_session)
        self.product_repository = ProductRepository(db_session)
        self.buyer_repository = BuyerRepository(db_session)
        self.order_item_repository = OrderItemRepository(db_session)
        self.product_size_repository = ProductSizeRepository(db_session)



    async def get_orders(self,
                   order_number: str = None,
                   buyer_email: str = None,) -> List[OrderSchema]:

        filters = remove_non_args(order_number = order_number,
                                  buyer = buyer_email)
        if 'buyer' in filters:
            buyer = await self.buyer_repository.get(email=buyer_email)
            if len(buyer) == 0:
                raise exceptions.NotFoundException("Buyer not found")

            filters['buyer'] = buyer

        orders = await self.order_repository.get(**filters, relationships=["order_items"])

        orders_schemas = []
        for order in orders:
            orders_schema = await self._model_to_schema(order)
            print(orders_schema)
            orders_schemas.append(orders_schema)
        return orders_schemas



    async def _is_existing_order_by_order_number(self, order_number: str) -> bool:
        product_list = await self.order_repository.get(order_number=order_number)
        return False if len(product_list) == 0 else True

    async def _reduce_from_stock(self, order_item: OrderItemSchema):

        product_size = await self.product_size_repository.get_product_size_by_size(product_id=order_item.product_id,
                                                                              size=order_item.size)

        if not product_size:
            raise exceptions.NotFoundException(f"Size {order_item.size.value} is not available for product {order_item.product_id}")
        if product_size.quantity_in_stock < order_item.quantity:
            raise exceptions.ForbiddenException(f"Not enough stock for size {order_item.size} of product {order_item.product_id}")


        new_product_quantity = product_size.quantity_in_stock - order_item.quantity
        return (await self.product_size_repository.update_product_stock(product_id=order_item.product_id,
                                                                        size=order_item.size,
                                                                        new_stock=new_product_quantity))

    async def create_order(self,
                     order: OrderSchema) -> OrderSchema:


        if await self._is_existing_order_by_order_number(order.order_number ):
            raise exceptions.DuplicateValueException("Order number already exists")

        #create_buyer
        buyer = await self.buyer_repository.get(email=order.buyer.email)
        if len(buyer)  == 0:
            buyer_created = await self.buyer_repository.create(obj_data=Buyer(name=order.buyer.name,
                                                                         email=order.buyer.email,
                                                                         phone=order.buyer.phone,))
        else:
            buyer_created = buyer[0]


        order_created = await self.order_repository.create(obj_data=Order(order_number=order.order_number,
                                                                    status=order.status,
                                                                    total_price=order.total_price,
                                                                    recipient_name=order.recipient_name,
                                                                    shipping_address=order.shipping_address,
                                                                    shipping_city=order.shipping_city,
                                                                    shipping_postal_code=order.shipping_postal_code,
                                                                    shipping_country=order.shipping_country,
                                                                    shipping_method=order.shipping_method,
                                                                    buyer_id=buyer_created.id))
        for order_item in order.order_items:
            print("create order item " + str(order_item))
            await self.order_item_repository.create(OrderItem(order_id=order_created.id,
                                                        product_id=order_item.product_id,
                                                        size=order_item.size,
                                                        price=order_item.price,
                                                        quantity=order_item.quantity))

            await self._reduce_from_stock(order_item=order_item)

        order_created = await self.order_repository.get(order_number=order.order_number, relationships=["order_items"])
        return await self._model_to_schema(order_created[0])


    @staticmethod
    def _schema_to_model(order_schema: OrderSchema):
        order_model = Order(order_number=order_schema.order_number,
                            status=order_schema.status,
                            total_price=order_schema.total_price,
                            recipient_name=order_schema.recipient_name,
                            shipping_address=order_schema.shipping_address,
                            shipping_city=order_schema.shipping_city,
                            shipping_postal_code=order_schema.shipping_postal_code,
                            shipping_country=order_schema.shipping_country,
                            shipping_method=order_schema.shipping_method,
                            buyer_id=order_schema.buyer.id)

        return order_model

    @staticmethod
    async def _model_to_schema(order_model: Order) -> OrderSchema:
        print(order_model.order_items)
        order_schema = OrderSchema(id=order_model.id,
                             order_number=order_model.order_number,
                             status=order_model.status,
                             total_price=order_model.total_price,
                             recipient_name=order_model.recipient_name,
                             shipping_address=order_model.shipping_address,
                             shipping_city=order_model.shipping_city,
                             shipping_postal_code=order_model.shipping_postal_code,
                             shipping_country=order_model.shipping_country,
                             shipping_method=order_model.shipping_method,
                             buyer=BuyerSchema(id=order_model.buyer.id,
                                               phone=order_model.buyer.phone,
                                               email=order_model.buyer.email,
                                               name=order_model.buyer.name,),
                             order_items=[OrderItemSchema(id=order_item_model.id,
                                                          quantity=order_item_model.quantity,
                                                          size=order_item_model.size,
                                                          price=order_item_model.price,
                                                          order_id=order_item_model.order_id,
                                                          product=ProductSchema.model_validate(order_item_model.product),
                                                          product_id=order_item_model.product_id) for order_item_model in order_model.order_items]
                             )
        return order_schema
