from typing import Annotated

from fastapi import APIRouter, Depends

from app.internal.factories import StatisticsFactory
from app.internal.services import StatisticsService
from app.internal.schemas import StatisticsSchema


router = APIRouter(
    prefix='/statistics',
    tags=['Statistics'],
)


@router.get('')
async def get_statistics(
    statistics_service: Annotated[StatisticsService, Depends(StatisticsFactory.get_statistics_service)],
) -> StatisticsSchema:
    statistics = await statistics_service.get_statistics()
    return statistics
