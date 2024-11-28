from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, BenefitContent, Option


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit

    async def get_benefit_with_rel(self, benefit_id: int) -> Benefit:
        query = (
            select(Benefit)
            .options(
                joinedload(Benefit.content),
                joinedload(Benefit.options)
            )
        )
        result = await self.session.scalar(query)
        return result


class BenefitContentRepository(SQLAlchemyRepository):
    model = BenefitContent


class OptionRepository(SQLAlchemyRepository):
    model = Option
