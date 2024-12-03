from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.s3_client import S3Client
from app.internal.repositories import CategoryRepository, UserRepository
from app.internal.services import CategoryService


class CategoryFactory:
    @staticmethod
    def get_category_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> CategoryService:
        return CategoryService(CategoryRepository, UserRepository, S3Client, session)
