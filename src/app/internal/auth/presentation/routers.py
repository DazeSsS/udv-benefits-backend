from typing import Annotated

from pydantic import EmailStr
from fastapi import APIRouter, BackgroundTasks, Depends, Response, Request, status

from app.internal.factories import AuthFactory
from app.internal.services import AuthService
from app.internal.auth.domain.schemas import TokenPairSchema


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/send-email')
async def send_email(
    email: EmailStr,
    auth_service: Annotated[AuthService, Depends(AuthFactory.get_auth_service)],
    background_tasks: BackgroundTasks,
):
    try:
        await auth_service.send_email(email=email, background_tasks=background_tasks)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content=f'{e}', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/token/login')
async def login(
    token: str,
    auth_service: Annotated[AuthService, Depends(AuthFactory.get_auth_service)],
) -> TokenPairSchema:
    tokens = await auth_service.login(token=token)
    return tokens


@router.post('/token/refresh')
async def refresh_tokens(
    refresh_token: str,
    auth_service: Annotated[AuthService, Depends(AuthFactory.get_auth_service)],
) -> TokenPairSchema:
    tokens = await auth_service.refresh_tokens(refresh_token=refresh_token)
    return tokens
