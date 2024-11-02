from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Order, User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_with_orders(self, user_id: int) -> User:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.orders)
            )
        )
        result = await self.session.scalar(query)
        return result

    async def get_user_with_benefits(self, user_id: int) -> User:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.orders).selectinload(Order.benefit)
            )
        )
        result = await self.session.scalar(query)
        return result
