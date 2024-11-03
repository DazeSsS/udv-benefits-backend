from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.email_client import EmailClient
from app.internal.repositories import (
    AuthRepository,
    BenefitRepository,
    CategoryRepository,
    OrderRepository,
    UserRepository,
)
from app.internal.services import (
    AuthService,
    BenefitService,
    CategoryService,
    OrderService,
    UserService,
)


def auth_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return AuthService(AuthRepository, UserRepository, EmailClient, session)

def category_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return CategoryService(CategoryRepository, session)

def order_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return OrderService(OrderRepository, session)

def user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(UserRepository, session)
