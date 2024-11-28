from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.email_client import EmailClient
from app.internal.repositories import CommentRepository, UserRepository
from app.internal.services import UserService


class UserFactory:
    @staticmethod
    def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
        return UserService(CommentRepository, UserRepository, EmailClient, session)
