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
