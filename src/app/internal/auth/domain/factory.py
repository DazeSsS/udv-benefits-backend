from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.email_client import EmailClient
from app.internal.repositories import AuthRepository, UserRepository
from app.internal.services import AuthService


class AuthFactory:
    @staticmethod
    def get_auth_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
        return AuthService(AuthRepository, UserRepository, EmailClient, session)
