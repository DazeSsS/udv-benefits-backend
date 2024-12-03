from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.s3_client import S3Client
from app.internal.models import Comment
from app.internal.repositories import AttachmentRepository, CommentRepository
from app.internal.schemas import CommentSchemaAdd, UserInfoSchema

from config import settings


class CommentService:
    def __init__(
        self,
        attachment_repo: AttachmentRepository,
        comment_repo: CommentRepository,
        s3_client: S3Client,
        session: AsyncSession,
    ):
        self.attachment_repo: AttachmentRepository = attachment_repo(session)
        self.comment_repo: CommentRepository = comment_repo(session)
        self.s3_client: S3Client = s3_client()

    async def add_comment(self, order_id: int, comment: CommentSchemaAdd, attachment: UploadFile | None, user_id: int):
        comment_dict = comment.model_dump()

        if attachment:
            file_url = await self.s3_client.upload(file=attachment, path=f'orders/{order_id}/')
            attachment_data = {
                'filename': attachment.filename,
                'file_url': file_url,
            }
            new_attachment = await self.attachment_repo.add(data=attachment_data)
            comment_dict.update(attachment_id=new_attachment.id)

        comment_dict.update(order_id=order_id, sender_id=user_id)
        comment = await self.comment_repo.add(data=comment_dict)
        return comment
