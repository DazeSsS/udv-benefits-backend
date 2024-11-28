from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.internal.repositories import CommentRepository, OrderRepository
from app.internal.services import CommentService


class CommentFactory:
    @staticmethod
    def get_comment_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> CommentService:
        return CommentService(CommentRepository, session)
