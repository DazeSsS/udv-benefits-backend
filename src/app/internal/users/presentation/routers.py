from typing import Annotated

from fastapi import APIRouter, Depends

from app.internal.dependencies import user_service
from app.internal.permissions import authorized_user, is_admin
from app.internal.users.domain.schemas import UserInfoSchema, UserSchema, UserSchemaAdd, UserSchemaUpdate
from app.internal.users.domain.services import UserService


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    # dependencies=[Depends(is_admin)]
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


@router.get('/unverified')
async def get_unverified_users(
    user_service: Annotated[UserService, Depends(user_service)],
) -> list[UserSchema]:
    users = await user_service.get_unverified_users()
    return users


@router.get('/me')
async def get_authorized_user(
    user_info: Annotated[UserInfoSchema, Depends(authorized_user)],
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    user = await user_service.get_user_by_id(user_id=user_info.id)
    return user


@router.get('/{id}')
async def get_user_by_id(
    id: int,
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    user = await user_service.get_user_by_id(user_id=id)
    return user


@router.patch('/{id}')
async def update_user_by_id(
    id: int,
    user: UserSchemaUpdate,
    user_service: Annotated[UserService, Depends(user_service)],
) -> UserSchema:
    updated_user = await user_service.update_user_by_id(user_id=id, new_data=user)
    return updated_user
