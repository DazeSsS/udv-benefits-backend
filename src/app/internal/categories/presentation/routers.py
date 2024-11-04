from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.internal.factories import CategoryFactory
from app.internal.benefits.domain.schemas import GroupedBenefitSchema
from app.internal.categories.domain.schemas import CategorySchema, CategorySchemaAdd
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
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
) -> GroupedBenefitSchema:
    grouped_benefits = await category_service.get_category_benefits_by_id(category_id=id)
    return grouped_benefits


@router.delete('/{id}')
async def delete_category_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(CategoryFactory.get_category_service)],
):
    await category_service.delete_category_by_id(category_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
