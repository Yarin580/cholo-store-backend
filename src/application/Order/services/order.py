from src.application.Order.enums import OrderStatus
from src.application.Order.models import OrderItem, Buyer, Order
from src.application.Order.repositories.Buyer import BuyerRepository
from src.application.Order.repositories.Order import OrderRepository
from src.application.Order.repositories.OrderItem import OrderItemRepository
from src.application.Order.schemas.buyer import BuyerSchema
from src.application.Order.schemas.order import OrderSchema, OrderItemSchema
from src.application.product.repositories.product_size import ProductSizeRepository
from src.application.product.services.product import ProductService

import src.modules.exceptions.base as exceptions

class OrderService:

    def __init__(self):
        self.order_repository = OrderRepository()
        self.product_size_repository = ProductSizeRepository()
        self.buyer_repository = BuyerRepository()
        self.order_item_repository = OrderItemRepository()


    def is_existing_order_by_order_number(self, order_number: str) -> bool:
        return False if len(self.order_repository.get(order_number=order_number)) == 0 else True


    def reduce_from_stock(self, order_item: OrderItemSchema):
        product_size = self.product_size_repository.get_product_size_by_size(product_id=order_item.product_id,
                                                                             size=order_item.size)

        if not product_size:
            raise exceptions.NotFoundException(f"Size {order_item.size.value} is not available for product {order_item.product_id}")

        if product_size.quantity_in_stock <= order_item.quantity:
            raise exceptions.ForbiddenException(f"Not enough stock for size {order_item.size} of product {order_item.product_id}")

        new_product_quantity = product_size.quantity_in_stock - order_item.quantity
        self.product_size_repository.update_product_stock(product_id=order_item.product_id,
                                                          size=order_item.size,
                                                          new_stock=new_product_quantity)

    def create_order(self,
                     order: OrderSchema) -> OrderSchema:

        if self.is_existing_order_by_order_number(order.order_number):
            raise exceptions.DuplicateValueException("Order number already exists")


        # for item in order.order_items:
        #     self.reduce_from_stock(order_item=item)


        buyer_created = self.buyer_repository.create(obj_data=Buyer(name=order.buyer.name,
                                                                    email=order.buyer.email,
                                                                    phone=order.buyer.phone,))

        try:
            order_created = self.order_repository.create(obj_data=Order(order_number=order.order_number,
                                                                        status=order.status,
                                                                        total_price=order.total_price,
                                                                        recipient_name=order.recipient_name,
                                                                        shipping_address=order.shipping_address,
                                                                        shipping_city=order.shipping_city,
                                                                        shipping_postal_code=order.shipping_postal_code,
                                                                        shipping_country=order.shipping_country,
                                                                        shipping_method=order.shipping_method,
                                                                        buyer_id=buyer_created.id))
        except Exception as e:
            self.buyer_repository.delete(obj_id=buyer_created.id)
            raise Exception("failed to create order")

        try:
            for order_item in order.order_items:
                self.order_item_repository.create(OrderItem(order_id=order_created.id,
                                                            product_id=order_item.product_id,
                                                            size=order_item.size,
                                                            price=order_item.price,
                                                            quantity=order_item.quantity))
        except Exception as e:
            for order_item in order.order_items:
                if len(self.order_item_repository.get(id=order_item.id)) != 0:
                    self.order_item_repository.delete(order_item.id)

            self.order_repository.delete(order_created.id)
            raise Exception("failed to create order")

        order_created = self.order_repository.get(order_number=order.order_number)

        return OrderSchema.model_validate(order_created)


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
