from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.orders.db.models import Status
from app.internal.repositories import BenefitRepository, CategoryRepository, UserRepository
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitType, BenefitSchemaAdd, BenefitSchemaUpdate, GroupedBenefitSchema


class BenefitService:
    def __init__(
        self, 
        benefit_repo: BenefitRepository,
        category_repo: CategoryRepository,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.category_repo: CategoryRepository = category_repo(session)
        self.user_repo: UserRepository = user_repo(session)

    async def add_benefit(self, benefit: BenefitSchemaAdd):
        benefit_dict = benefit.model_dump()
        benefit = await self.benefit_repo.add(data=benefit_dict)
        return benefit

    async def get_benefit_by_id(self, benefit_id: int):
        benefit = await self.benefit_repo.get_benefit_with_category(benefit_id=benefit_id)
        return benefit

    async def get_benefits(self):
        benefits = await self.benefit_repo.get_benefits_with_categories()
        return benefits

    async def get_grouped_benefits(self, user_id: int | None, benefit_type: str):
        categories = await self.category_repo.get_categories_with_benefits()

        if user_id:
            user = await self.user_repo.get_user_with_benefits(user_id=user_id)
        else:
            user = None

        grouped_benefits = []
        for category in categories:
            if benefit_type == BenefitType.AVAILABLE and user:
                category_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=category.benefits,
                )
                grouped_benefits.append(category_benefits)
            elif benefit_type == BenefitType.ACTIVE and user:
                user_benefit_ids = []
                for order in user.orders:
                    if order.status == Status.APPROVED:
                        user_benefit_ids.append(order.benefit.id)

                user_benefits = []
                for benefit in category.benefits:
                    if benefit.id in user_benefit_ids:
                        user_benefits.append(benefit)

                category_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=user_benefits,
                )
                grouped_benefits.append(category_benefits)
            else:
                category_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=category.benefits,
                )
                grouped_benefits.append(category_benefits)

        return grouped_benefits

    async def update_benefit_by_id(self, benefit_id: int, new_data: BenefitSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_benefit = await self.benefit_repo.update_by_id(id=benefit_id, new_data=new_data_dict)
        return updated_benefit

    async def delete_benefit_by_id(self, benefit_id: int):
        await self.benefit_repo.delete_by_id(id=benefit_id)
