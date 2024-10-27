from app.repository import SQLAlchemyRepository
from app.models import Comment


class CommentRepository(SQLAlchemyRepository):
    model = Comment
