from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from app.dependencies import benefit_service
from app.benefits.domain.schemas import BenefitSchema, BenefitSchemaAdd
from app.benefits.domain.services import BenefitService


router = APIRouter(
    prefix='/benefits',
    tags=['Benefits'],
)


@router.post('')
async def add_benefit(
    benefit: BenefitSchemaAdd,
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> BenefitSchema:
    new_benefit = await benefit_service.add_benefit(benefit)
    return new_benefit


@router.get('')
async def get_benefits(
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> list[BenefitSchema]:
    benefits = await benefit_service.get_benefits()
    return benefits
