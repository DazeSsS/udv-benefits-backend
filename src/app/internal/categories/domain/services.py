from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.categories.db.repositories import CategoryRepository
from app.internal.categories.domain.schemas import CategorySchemaAdd


class CategoryService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        session: AsyncSession,
    ):
        self.category_repo: CategoryRepository = category_repo(session)

    async def add_category(self, category: CategorySchemaAdd):
        category_dict = category.model_dump()
        category = await self.category_repo.add(data=category_dict)
        return category

    async def get_categories(self):
        categories = await self.category_repo.get_all()
        return categories