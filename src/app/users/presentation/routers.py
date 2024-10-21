from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import user_service
from app.users.domain.schemas import UserSchema, UserSchemaAdd
from app.users.domain.services import UserService


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('')
async def add_user(
    user: UserSchemaAdd,
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    new_user = await user_service.add_user(user)
    return new_user


@router.get('')
async def get_categories(
    user_service: Annotated[UserService, Depends(user_service)],
) -> list[UserSchema]:
    users = await user_service.get_users()
    return users
