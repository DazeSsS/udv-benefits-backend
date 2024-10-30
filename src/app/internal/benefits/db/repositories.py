from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit
