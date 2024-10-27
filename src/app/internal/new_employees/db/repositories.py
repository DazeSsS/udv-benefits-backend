from app.repository import SQLAlchemyRepository
from app.models import NewEmployee


class NewEmployeeRepository(SQLAlchemyRepository):
    model = NewEmployee
