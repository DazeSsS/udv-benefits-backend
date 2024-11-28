from app.schema import BaseSchema


class CategorySchemaAdd(BaseSchema):
    title: str


class CategorySchema(CategorySchemaAdd):
    id: int
