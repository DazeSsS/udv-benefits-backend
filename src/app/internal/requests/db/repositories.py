from app.repository import SQLAlchemyRepository
from app.internal.models import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request
