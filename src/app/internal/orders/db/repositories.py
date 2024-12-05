from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, Comment, Order
from app.internal.schemas import Status


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_order_with_benefit(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.user),
                joinedload(Order.benefit).joinedload(Benefit.category),
                joinedload(Order.benefit).joinedload(Benefit.content)
            )
        )
        result = await self.session.scalar(query)
        return result

    async def get_order_with_related(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.option),
                joinedload(Order.benefit).joinedload(Benefit.category),
                joinedload(Order.benefit).joinedload(Benefit.content),
                joinedload(Order.benefit).joinedload(Benefit.options),
                selectinload(Order.comments)
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

    async def get_order_with_comments(self, order_id: int) -> Order:
        query = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.comments),
            )
        )
        result = await self.session.scalar(query)
        return result

    async def get_active_orders_count(self) -> int:
        query = (
            select(func.count())
            .select_from(Order)
            .where(Order.status == Status.APPROVED)
        )
        result = await self.session.scalar(query)
        return result
