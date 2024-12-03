from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, status, UploadFile

from app.internal.access import get_current_user
from app.internal.factories import BenefitFactory, CategoryFactory
from app.internal.benefits.domain.schemas import BenefitType, GroupedBenefitSchema
from app.internal.categories.domain.schemas import CategorySchema, CategorySchemaAdd
from app.internal.users.domain.schemas import UserInfoSchema
from app.internal.services import BenefitService, CategoryService


router = APIRouter(
    prefix='/categories',
    tags=['Categories'],
)


@router.post('')
async def add_category(
    title: Annotated[str, Form()],
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
    icon: Annotated[UploadFile | None, File()] = None,
) -> CategorySchema:
    category = CategorySchemaAdd(title=title)
    new_category = await category_service.add_category(category=category, icon=icon)
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
    benefit_service: Annotated[BenefitService, Depends(BenefitFactory.get_benefit_service)],
    benefit_type: BenefitType = BenefitType.AVAILABLE,
) -> GroupedBenefitSchema:
    grouped_benefits = await benefit_service.get_category_benefits_by_id(
        user_id=user_info.id,
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
