from sqlalchemy import desc, func, select
from sqlalchemy.orm import joinedload, selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import Benefit, BenefitContent, Option, Order
from app.internal.schemas import Status


class BenefitRepository(SQLAlchemyRepository):
    model = Benefit

    async def get_benefit_with_rel(self, benefit_id: int) -> Benefit:
        query = (
            select(Benefit)
            .where(Benefit.id == benefit_id)
            .options(
                joinedload(Benefit.content),
                selectinload(Benefit.options)
            )
        )
        result = await self.session.scalar(query)
        return result

    async def get_benefits_with_rel(self) -> list[Benefit]:
        query = (
            select(Benefit)
            .options(
                joinedload(Benefit.content),
                selectinload(Benefit.options)
            )
            .order_by(Benefit.created_at.desc(), Benefit.id.desc())
        )
        result = await self.session.scalars(query)
        return result.all()

    async def get_total_benefits_count(self) -> int:
        query = (
            select(func.count())
            .select_from(Benefit)
        )
        result = await self.session.scalar(query)
        return result

    async def get_most_popular_benefit(self):
        subquery = (
            select(
                Order.benefit_id,
                func.count(Order.id).label("order_count")
            )
            .group_by(Order.benefit_id)
        ).subquery()

        query = (
            select(Benefit, subquery.c.order_count)
            .join(subquery, Benefit.id == subquery.c.benefit_id)
            .order_by(desc(subquery.c.order_count))
            .limit(1)
        )
        result = await self.session.scalar(query)
        return result


class BenefitContentRepository(SQLAlchemyRepository):
    model = BenefitContent


class OptionRepository(SQLAlchemyRepository):
    model = Option
