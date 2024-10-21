from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.categories.db.repositories import CategoryRepository
from app.categories.domain.services import CategoryService
from app.benefits.db.repositories import BenefitRepository
from app.benefits.domain.services import BenefitService
from app.users.db.repositories import UserRepository
from app.users.domain.services import UserService


def category_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return CategoryService(CategoryRepository, session)

def benefit_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return BenefitService(BenefitRepository, session)

def user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return UserService(UserRepository, session)
