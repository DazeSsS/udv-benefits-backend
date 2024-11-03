from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Category


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
