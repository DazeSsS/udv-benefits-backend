from app.repository import SQLAlchemyRepository
from app.internal.models import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category
