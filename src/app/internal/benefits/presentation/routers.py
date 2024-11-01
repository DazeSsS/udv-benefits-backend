from typing import Union

from fastapi import APIRouter, Depends, Response, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.dependencies import benefit_service
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitSchemaAdd, BenefitSchemaUpdate, GroupedBenefitSchema
from app.internal.benefits.domain.services import BenefitService


router = APIRouter(
    prefix='/benefits',
    tags=['Benefits'],
)


@router.post('')
async def add_benefit(
    benefit: BenefitSchemaAdd,
    benefit_service: BenefitService = Depends(benefit_service),
) -> BenefitSchema:
    new_benefit = await benefit_service.add_benefit(benefit)
    return new_benefit


@router.get('')
async def get_benefits(
    benefit_service: BenefitService = Depends(benefit_service),
) -> list[BenefitSchema]:
    benefits = await benefit_service.get_benefits()
    return benefits


@router.get('/grouped')
async def get_grouped_benefits(
    benefit_service: BenefitService = Depends(benefit_service),
) -> list[GroupedBenefitSchema]:
    grouped_benefits = await benefit_service.get_grouped_benefits()
    return grouped_benefits


@router.get('/{id}')
async def get_benefit_by_id(
    id: int,
    benefit_service: BenefitService = Depends(benefit_service),
) -> BenefitSchema:
    benefit = await benefit_service.get_benefit_by_id(benefit_id=id)
    return benefit


@router.patch('/{id}')
async def update_benefit_by_id(
    id: int,
    benefit: BenefitSchemaUpdate,
    benefit_service: BenefitService = Depends(benefit_service),
) -> BenefitSchema:
    updated_benefit = await benefit_service.update_benefit_by_id(benefit_id=id, new_data=benefit)
    return updated_benefit


@router.delete('/{id}')
async def delete_benefit_by_id(
    id: int,
    benefit_service: BenefitService = Depends(benefit_service),
):
    await benefit_service.delete_benefit_by_id(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
