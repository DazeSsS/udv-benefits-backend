from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import SQLAlchemyRepository
from app.categories.domain.schemas import CategorySchemaAdd


class CategoryService:
    def __init__(
        self,
        category_repo: SQLAlchemyRepository,
        session: AsyncSession,
    ):
        self.category_repo: SQLAlchemyRepository = category_repo(session)

    async def add_category(self, category: CategorySchemaAdd):
        category_dict = category.model_dump()
        category = await self.category_repo.add(category_dict)
        return category

    async def get_categories(self):
        categories = await self.category_repo.get_all()
        return categories