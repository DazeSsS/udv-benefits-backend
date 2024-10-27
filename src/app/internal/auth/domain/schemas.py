from pydantic import BaseModel


class CategorySchemaAdd(BaseModel):
    title: str


class CategorySchema(CategorySchemaAdd):
    id: int
