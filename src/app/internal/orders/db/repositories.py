from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, Order


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_order_with_related(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.user),
                joinedload(Order.benefit).joinedload(Benefit.category)
            )
        )
        result = await self.session.scalar(query)
        return result

    async def get_all_orders_with_related(self) -> list[Order]:
        query = (
            select(Order)
            .options(
                joinedload(Order.user),
                joinedload(Order.benefit).joinedload(Benefit.category)
            )
            .order_by(Order.created_at.desc())
        )
        result = await self.session.scalars(query)
        return result.all()
