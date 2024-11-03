from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.access import get_current_user, is_authorized
from app.internal.factories import BenefitFactory
from app.internal.services import BenefitService
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitType, BenefitSchemaAdd, BenefitSchemaUpdate, GroupedBenefitSchema
from app.internal.users.domain.schemas import UserInfoSchema


router = APIRouter(
    prefix='/benefits',
    tags=['Benefits'],
)


@router.post('')
async def add_benefit(
    benefit: BenefitSchemaAdd,
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
) -> BenefitSchema:
    new_benefit = await benefit_service.add_benefit(benefit=benefit)
    return new_benefit


@router.get('')
async def get_benefits(
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
) -> list[BenefitSchema]:
    benefits = await benefit_service.get_benefits()
    return benefits


@router.get('/grouped')
async def get_grouped_benefits(
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
    benefit_type: BenefitType = BenefitType.AVAILABLE,
) -> list[GroupedBenefitSchema]:
    grouped_benefits = await benefit_service.get_grouped_benefits(
        user_id=user_info.id if user_info else None,
        benefit_type=benefit_type,
    )
    return grouped_benefits


@router.get('/{id}')
async def get_benefit_by_id(
    id: int,
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
) -> BenefitSchema:
    benefit = await benefit_service.get_benefit_by_id(benefit_id=id)
    return benefit


@router.patch('/{id}')
async def update_benefit_by_id(
    id: int,
    benefit: BenefitSchemaUpdate,
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
) -> BenefitSchema:
    updated_benefit = await benefit_service.update_benefit_by_id(benefit_id=id, new_data=benefit)
    return updated_benefit


@router.delete('/{id}')
async def delete_benefit_by_id(
    id: int,
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
):
    await benefit_service.delete_benefit_by_id(benefit_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
