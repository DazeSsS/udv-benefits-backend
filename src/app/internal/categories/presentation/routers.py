from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.internal.access import get_current_user
from app.internal.factories import CategoryFactory
from app.internal.benefits.domain.schemas import BenefitType, GroupedBenefitSchema
from app.internal.categories.domain.schemas import CategorySchema, CategorySchemaAdd
from app.internal.users.domain.schemas import UserInfoSchema
from app.internal.services import CategoryService


router = APIRouter(
    prefix='/categories',
    tags=['Categories'],
)


@router.post('')
async def add_category(
    category: CategorySchemaAdd,
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
) -> CategorySchema:
    new_category = await category_service.add_category(category)
    return new_category


@router.get('')
async def get_categories(
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
) -> list[CategorySchema]:
    categories = await category_service.get_categories()
    return categories


@router.get('/{id}')
async def get_category_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
) -> CategorySchema:
    category = await category_service.get_category_by_id(category_id=id)
    return category


@router.get('/{id}/benefits')
async def get_category_benefits_by_id(
    id: int,
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
    benefit_type: BenefitType = BenefitType.AVAILABLE,
) -> GroupedBenefitSchema:
    grouped_benefits = await category_service.get_category_benefits_by_id(
        user_id=user_info.id if user_info else None,
        category_id=id,
        benefit_type=benefit_type,
    )
    return grouped_benefits


@router.delete('/{id}')
async def delete_category_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
):
    await category_service.delete_category_by_id(category_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
