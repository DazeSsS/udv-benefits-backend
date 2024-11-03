from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.internal.repositories import BenefitRepository, CategoryRepository, UserRepository
from app.internal.services import BenefitService


class BenefitFactory:
    @staticmethod
    def get_benefit_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
        return BenefitService(BenefitRepository, CategoryRepository, UserRepository, session)
