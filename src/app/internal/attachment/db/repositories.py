from app.repository import SQLAlchemyRepository
from app.internal.models import Attachment


class AttachmentRepository(SQLAlchemyRepository):
    model = Attachment
