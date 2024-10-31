import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2AuthorizationCodeBearer

from config import settings

from app.internal.auth.domain.services import AuthService
from app.internal.users.domain.schemas import UserInfoSchema


def authorized_user(request: Request):
    if settings.PUBLIC_API:
        return

    token = request.state.token
    if not token:
        raise HTTPException(status_code=401, detail='Authorization token was not provided')
    
    try:
        payload = AuthService.get_payload(token)
        user_id = payload.get('user_id')
        is_admin = payload.get('is_admin')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    return UserInfoSchema(id=user_id, is_admin=is_admin)


def is_admin(user: Annotated[UserInfoSchema, Depends(authorized_user)]):
    if settings.PUBLIC_API:
        return

    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Admin permissions required')
