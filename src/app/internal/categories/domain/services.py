from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.s3_client import S3Client
from app.internal.orders.domain.schemas import Status
from app.internal.repositories import CategoryRepository, UserRepository
from app.internal.categories.domain.schemas import CategorySchemaAdd
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitType, GroupedBenefitSchema


class CategoryService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        user_repo: UserRepository,
        s3_client: S3Client,
        session: AsyncSession,
    ):
        self.category_repo: CategoryRepository = category_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.s3_client: S3Client = s3_client()

    async def add_category(self, category: CategorySchemaAdd, icon: UploadFile | None):
        category_dict = category.model_dump()

        if icon:
            file_url = await self.s3_client.upload(file=icon, path=f'categories/')
            category_dict.update(icon=file_url)

        category = await self.category_repo.add(data=category_dict)
        return category

    async def get_categories(self):
        categories = await self.category_repo.get_all()
        return categories

    async def get_category_by_id(self, category_id: int):
        category = await self.category_repo.get_by_id(id=category_id)
        return category

    async def delete_category_by_id(self, category_id: int):
        await self.category_repo.delete_by_id(id=category_id)
