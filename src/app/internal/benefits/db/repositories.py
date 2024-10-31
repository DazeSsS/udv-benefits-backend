from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit

    async def get_benefits_with_categories(self):
        query = (
            select(self.model)
            .options(joinedload(self.model.category))
        )
        result = self.session.scalars(query)
        return result.all()
