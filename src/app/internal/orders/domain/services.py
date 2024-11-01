from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.orders.db.repositories import OrderRepository
from app.internal.orders.domain.schemas import OrderSchemaAdd


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: AsyncSession,
    ):
        self.order_repo: OrderRepository = order_repo(session)

    async def add_order(self, category: OrderSchemaAdd):
        pass
