from datetime import datetime

from app.schema import BaseSchema
from app.internal.users.domain.schemas import UserSchemaShort


class CommentSchemaAdd(BaseSchema):
    message: str


class CommentSchema(CommentSchemaAdd):
    id: int
    is_read: bool
    created_at: datetime


class CommentSchemaRel(CommentSchema):
    sender: UserSchemaShort
