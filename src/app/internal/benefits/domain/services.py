from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.benefits.db.repositories import BenefitRepository
from app.internal.categories.db.repositories import CategoryRepository
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitSchemaAdd, BenefitSchemaUpdate, GroupedBenefitSchema


class BenefitService:
    def __init__(
        self, 
        benefit_repo: BenefitRepository,
        category_repo: CategoryRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.category_repo: CategoryRepository = category_repo(session)

    async def add_benefit(self, benefit: BenefitSchemaAdd):
        benefit_dict = benefit.model_dump()
        benefit = await self.benefit_repo.add(data=benefit_dict)
        return benefit

    async def get_benefit_by_id(self, benefit_id: int):
        benefit = await self.benefit_repo.get_by_id(id=benefit_id)
        return benefit

    async def get_benefits(self):
        benefits = await self.benefit_repo.get_all()
        return benefits

    async def get_grouped_benefits(self):
        categories = await self.category_repo.get_categories_with_benefits()

        grouped_benefits = [
            GroupedBenefitSchema(
                category_id=category.id,
                category_title=category.title,
                benefits=[
                    BenefitSchema.model_validate(benefit)
                    for benefit in category.benefits
                ]
            )
            for category in categories
        ]

        return grouped_benefits

    async def update_benefit_by_id(self, benefit_id: int, new_data: BenefitSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_benefit = await self.benefit_repo.update_by_id(id=benefit_id, new_data=new_data_dict)
        return updated_benefit

    async def delete_benefit_by_id(self, benefit_id: int):
        await self.benefit_repo.delete_by_id(id=benefit_id)
        return
