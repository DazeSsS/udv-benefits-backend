from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import category_service
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
