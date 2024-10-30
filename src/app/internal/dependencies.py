from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.email_client import EmailClient
from app.internal.auth.db.repositories import AuthRepository
from app.internal.auth.domain.services import AuthService
from app.internal.categories.db.repositories import CategoryRepository
from app.internal.categories.domain.services import CategoryService
from app.internal.benefits.db.repositories import BenefitRepository
from app.internal.benefits.domain.services import BenefitService
from app.internal.users.db.repositories import UserRepository
from app.internal.users.domain.services import UserService


def auth_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return AuthService(AuthRepository, UserRepository, EmailClient, session)

def category_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return CategoryService(CategoryRepository, session)

def benefit_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return BenefitService(BenefitRepository, session)

def user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(UserRepository, session)
