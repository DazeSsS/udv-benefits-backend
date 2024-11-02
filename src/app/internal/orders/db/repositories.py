from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Order


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_order_with_user_and_benefit(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.user),
                joinedload(Order.benefit)
            )
        )
        result = await self.session.scalar(query)
        return result
