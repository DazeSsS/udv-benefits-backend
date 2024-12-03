from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.s3_client import S3Client
from app.internal.repositories import BenefitRepository, BenefitContentRepository, OptionRepository, CategoryRepository, UserRepository
from app.internal.services import BenefitService


class BenefitFactory:
    @staticmethod
    def get_benefit_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> BenefitService:
        return BenefitService(
            BenefitRepository,
            BenefitContentRepository,
            OptionRepository,
            CategoryRepository,
            UserRepository,
            S3Client,
            session
        )
