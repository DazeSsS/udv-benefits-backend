from typing import Annotated

from fastapi import APIRouter, Depends

from app.internal.dependencies import user_service
from app.internal.permissions import authorized_user
from app.internal.users.domain.schemas import UserInfoSchema, UserSchema, UserSchemaAdd
from app.internal.users.domain.services import UserService


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('')
async def add_user(
    user: UserSchemaAdd,
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    new_user = await user_service.add_user(user=user)
    return new_user


@router.get('')
async def get_users(
    user_service: Annotated[UserService, Depends(user_service)],
) -> list[UserSchema]:
    users = await user_service.get_users()
    return users


@router.get('/me')
async def get_authorized_user(
    user_info: Annotated[UserInfoSchema, Depends(authorized_user)],
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    user = await user_service.get_user_by_id(user_id=user_info.id)
    return user
