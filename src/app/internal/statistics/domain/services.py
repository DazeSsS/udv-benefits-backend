from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.repositories import BenefitRepository, CategoryRepository, OrderRepository, UserRepository
from app.internal.schemas import CategoryStatistics


class StatisticsService:
    def __init__(
        self,
        benefit_repo: BenefitRepository,
        category_repo: CategoryRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.category_repo: CategoryRepository = category_repo(session)
        self.order_repo: OrderRepository = order_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.session = session

    async def get_statistics(self):
        statistics = {}

        statistics['active_benefits'] = await self.order_repo.get_active_orders_count()
        statistics['total_benefits'] = await self.benefit_repo.get_total_benefits_count()
        statistics['total_users'] = await self.user_repo.get_total_users_count()
        statistics['popular_benefit'] = await self.benefit_repo.get_most_popular_benefit()

        statistics['category_statistics'] = []
        categories = await self.category_repo.get_all()
        for category in categories:
            active_benefits = await self.category_repo.get_active_benefits_by_id(category_id=category.id)
            statistics['category_statistics'].append(
                CategoryStatistics(
                    category=category,
                    active_benefits=active_benefits
                )
            )

        return statistics
