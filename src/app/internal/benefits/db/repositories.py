from app.repository import SQLAlchemyRepository
from app.models import Benefit


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit
