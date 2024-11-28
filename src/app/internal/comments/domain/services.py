from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.models import Comment
from app.internal.repositories import CommentRepository, OrderRepository
from app.internal.schemas import CommentSchemaAdd, UserInfoSchema

from config import settings


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository,
        session: AsyncSession,
    ):
        self.comment_repo: CommentRepository = comment_repo(session)

    async def add_comment(self, order_id: int, comment: CommentSchemaAdd, user_id: int):
        comment_dict = comment.model_dump()
        comment_dict.update(order_id=order_id, sender_id=user_id)
        comment = await self.comment_repo.add(data=comment_dict)
        return comment
