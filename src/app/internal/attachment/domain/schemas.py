from app.schema import BaseSchema


class AttachmentSchemaAdd(BaseSchema):
    filename: str
    file_url: str


class AttachmentSchema(AttachmentSchemaAdd):
    id: int
