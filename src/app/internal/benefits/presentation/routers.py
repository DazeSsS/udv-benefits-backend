from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import benefit_service
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitSchemaAdd
from app.internal.benefits.domain.services import BenefitService


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


@router.get('/{id}')
async def get_benefit_by_id(
    id: int,
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> BenefitSchema:
    benefit = await benefit_service.get_benefit_by_id(id)
    return benefit


@router.get('')
async def get_benefits(
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> list[BenefitSchema]:
    benefits = await benefit_service.get_benefits()
    return benefits


@router.put('/{id}')
async def update_benefit_by_id(
    id: int,
    benefit: BenefitSchemaAdd,
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> BenefitSchema:
    updated_benefit = await benefit_service.update_benefit_by_id(id, benefit)
    return updated_benefit


@router.delete('/{id}')
async def delete_benefit_by_id(
    id: int,
    benefit_service: Annotated[BenefitService, Depends(benefit_service)],
) -> None:
    await benefit_service.delete_benefit_by_id(id)
