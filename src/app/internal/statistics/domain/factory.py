from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.internal.repositories import BenefitRepository, CategoryRepository, OrderRepository, UserRepository
from app.internal.services import StatisticsService


class StatisticsFactory:
    @staticmethod
    def get_statistics_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> StatisticsService:
        return StatisticsService(BenefitRepository, CategoryRepository, OrderRepository, UserRepository, session)
