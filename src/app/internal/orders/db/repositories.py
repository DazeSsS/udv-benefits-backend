from app.repository import SQLAlchemyRepository
from app.internal.models import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order
