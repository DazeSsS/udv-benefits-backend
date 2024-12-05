from sqlalchemy import func, select, update
from sqlalchemy.orm import selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, Order, User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_with_related(self, user_id: int) -> User:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.orders)
                .joinedload(Order.benefit)
                .joinedload(Benefit.category)
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

    async def get_all_users(self) -> list[User]:
        query = (
            select(User)
            .order_by(User.is_verified, User.created_at.desc())
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_unverified_users(self) -> list[User]:
        query = (
            select(User)
            .where(User.is_verified == False)
            .order_by(User.created_at.desc())
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_total_users_count(self) -> int:
        query = (
            select(func.count())
            .select_from(User)
        )
        result = await self.session.scalar(query)
        return result
