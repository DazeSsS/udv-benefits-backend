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

    async def get_benefit_with_category(self, benefit_id: int):
        query = (
            select(Benefit)
            .where(Benefit.id == benefit_id)
            .options(joinedload(Benefit.category))
        )
        result = await self.session.scalar(query)
        return result
