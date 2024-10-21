from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import AbstractRepository
from app.benefits.domain.schemas import BenefitSchemaAdd


class BenefitService:
    def __init__(
        self, 
        benefit_repo: AbstractRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: AbstractRepository = benefit_repo(session)

    async def add_benefit(self, benefit: BenefitSchemaAdd):
        benefit_dict = benefit.model_dump()
        benefit = await self.benefit_repo.add(benefit_dict)
        return benefit

    async def get_benefit_by_id(self, id: int):
        benefit = await self.benefit_repo.get_by_id(id)
        return benefit

    async def get_benefits(self):
        benefits = await self.benefit_repo.get_all()
        return benefits