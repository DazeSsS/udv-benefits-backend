from app.repository import SQLAlchemyRepository
from app.models import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category
