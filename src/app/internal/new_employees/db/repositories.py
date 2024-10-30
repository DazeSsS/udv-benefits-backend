from app.repository import SQLAlchemyRepository
from app.internal.models import NewEmployee


class NewEmployeeRepository(SQLAlchemyRepository):
    model = NewEmployee
