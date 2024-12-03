from datetime import datetime

from app.schema import BaseSchema
from app.internal.users.domain.schemas import UserSchemaShort
from app.internal.attachment.domain.schemas import AttachmentSchema


class CommentSchemaAdd(BaseSchema):
    message: str


class CommentSchema(CommentSchemaAdd):
    id: int
    is_read: bool
    created_at: datetime
    attachment_id: int | None


class CommentSchemaRel(CommentSchema):
    sender: UserSchemaShort
    attachment: AttachmentSchema | None
