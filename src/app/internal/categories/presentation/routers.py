from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.internal.dependencies import category_service
from app.internal.benefits.domain.schemas import BenefitSchema
from app.internal.categories.domain.schemas import CategorySchema, CategorySchemaAdd
from app.internal.categories.domain.services import CategoryService


router = APIRouter(
    prefix='/categories',
    tags=['Categories'],
)


@router.post('')
async def add_category(
    category: CategorySchemaAdd,
    category_service: Annotated[CategoryService, Depends(category_service)],
) -> CategorySchema:
    new_category = await category_service.add_category(category)
    return new_category


@router.get('')
async def get_categories(
    category_service: Annotated[CategoryService, Depends(category_service)],
) -> list[CategorySchema]:
    categories = await category_service.get_categories()
    return categories


@router.get('/{id}')
async def get_category_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(category_service)],
) -> CategorySchema:
    category = await category_service.get_category_by_id(category_id=id)
    return category


@router.get('/{id}/benefits')
async def get_category_benefits_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(category_service)],
) -> list[BenefitSchema]:
    benefits = await category_service.get_category_benefits_by_id(category_id=id)
    return benefits


@router.delete('/{id}')
async def delete_category_by_id(
    id: int,
    category_service: Annotated[CategoryService, Depends(category_service)],
):
    await category_service.delete_category_by_id(category_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
