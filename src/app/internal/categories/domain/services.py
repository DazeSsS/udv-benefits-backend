from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.orders.domain.schemas import Status
from app.internal.repositories import CategoryRepository, UserRepository
from app.internal.categories.domain.schemas import CategorySchemaAdd
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitType, GroupedBenefitSchema


class CategoryService:
    def __init__(
        self,
        category_repo: CategoryRepository,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.category_repo: CategoryRepository = category_repo(session)
        self.user_repo: UserRepository = user_repo(session)

    async def add_category(self, category: CategorySchemaAdd):
        category_dict = category.model_dump()
        category = await self.category_repo.add(data=category_dict)
        return category

    async def get_categories(self):
        categories = await self.category_repo.get_all()
        return categories

    async def get_category_by_id(self, category_id: int):
        category = await self.category_repo.get_by_id(id=category_id)
        return category

    async def get_category_benefits_by_id(self, user_id: int | None, category_id: int, benefit_type: BenefitType):
        category = await self.category_repo.get_category_with_benefits_by_id(category_id=category_id)

        if not category.benefits:
            return # TODO

        if user_id:
            user = await self.user_repo.get_user_with_benefits(user_id=user_id)
        else:
            user = None

        if benefit_type == BenefitType.AVAILABLE and user:
            grouped_benefits = GroupedBenefitSchema(
                category_id=category.id,
                category_title=category.title,
                benefits=[
                    BenefitSchema.model_validate(benefit)
                    for benefit in category.benefits
                ]
            )
        elif benefit_type == BenefitType.ACTIVE and user:
            user_benefit_ids = []
            for order in user.orders:
                if order.status == Status.APPROVED:
                    user_benefit_ids.append(order.benefit.id)

            user_benefits = []
            for benefit in category.benefits:
                if benefit.id in user_benefit_ids:
                    user_benefits.append(benefit)

            grouped_benefits = GroupedBenefitSchema(
                category_id=category.id,
                category_title=category.title,
                benefits=user_benefits,
            )
        else:
            grouped_benefits = GroupedBenefitSchema(
                category_id=category.id,
                category_title=category.title,
                benefits=[
                    BenefitSchema.model_validate(benefit)
                    for benefit in category.benefits
                ]
            )

        return grouped_benefits

    async def delete_category_by_id(self, category_id: int):
        await self.category_repo.delete_by_id(id=category_id)
