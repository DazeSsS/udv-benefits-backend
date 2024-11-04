from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit

    async def get_benefits_with_categories(self):
        query = (
            select(Benefit)
            .options(joinedload(Benefit.category))
        )
        result = await self.session.scalars(query)
        return result.all()
