from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Comment


class CommentRepository(SQLAlchemyRepository):
    model = Comment

    async def get_comments_by_order_id(self, order_id: int) -> list[Comment]:
        query = (
            select(Comment)
            .where(Comment.order_id == order_id)
            .options(joinedload(Comment.sender))
            .order_by(Comment.created_at.desc())
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_unread_comments_by_order_id(self, order_id: int, user_id: int) -> list[Comment]:
        query = (
            select(Comment)
            .where(
                (Comment.order_id == order_id) &
                (Comment.sender_id != user_id) &
                (Comment.is_read == False)
            )
            .order_by(Comment.created_at.desc())
        )
        result = await self.session.scalars(query)
        return result.all()
