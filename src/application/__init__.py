from src.modules.db.base_model import Base
from src.application.product.models import Product,ProductSize,Category
from src.application.user.models import User
from src.application.Order.models import Order,OrderItem,Buyer

from src.modules.db.database_base import engine

def init_app():
    Base.metadata.drop_all(bind=engine)