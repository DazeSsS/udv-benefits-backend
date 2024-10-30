from app.repository import SQLAlchemyRepository
from app.internal.models import Comment


class CommentRepository(SQLAlchemyRepository):
    model = Comment
