from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, Category, Order
from app.internal.schemas import Status


class CategoryRepository(SQLAlchemyRepository):
    model = Category

    async def get_categories_with_benefits(self):
        query = (
            select(Category)
            .options(selectinload(Category.benefits))
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_category_with_benefits_by_id(self, category_id: int):
        query = (
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.benefits))
        )
        result = await self.session.scalar(query)
        return result

    async def get_active_benefits_by_id(self, category_id: int):
        query = (
            select(func.count(Order.id))
            .join(Benefit, Benefit.id == Order.benefit_id)
            .where(
                (Benefit.category_id == category_id) & 
                (Order.status == Status.APPROVED)
            )
        )
        result = await self.session.scalar(query)
        return result
