from app.repository import SQLAlchemyRepository
from app.models import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
