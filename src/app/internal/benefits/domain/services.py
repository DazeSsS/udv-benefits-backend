from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import AbstractRepository
from app.internal.benefits.db.repositories import BenefitRepository
from app.internal.benefits.domain.schemas import BenefitSchemaAdd


class BenefitService:
    def __init__(
        self, 
        benefit_repo: BenefitRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)

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

    async def update_benefit_by_id(self, id: int, new_data: BenefitSchemaAdd):
        new_data_dict = new_data.model_dump()
        updated_benefit = await self.benefit_repo.update_by_id(id, new_data_dict)
        return updated_benefit

    async def delete_benefit_by_id(self, id: int):
        deleted = await self.benefit_repo.delete_by_id(id)
        return deleted
