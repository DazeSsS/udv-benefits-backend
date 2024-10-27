from app.repository import SQLAlchemyRepository
from app.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
