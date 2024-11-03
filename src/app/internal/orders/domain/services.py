from zoneinfo import ZoneInfo
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.repositories import OrderRepository
from app.internal.orders.domain.schemas import OrderSchemaAdd, OrderSchemaUpdate
from app.internal.orders.db.models import Status
from app.internal.benefits.db.models import PERIOD_MAP

from config import settings


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        session: AsyncSession,
    ):
        self.order_repo: OrderRepository = order_repo(session)
        self.session = session

    async def add_order(self, order: OrderSchemaAdd):
        order_dict = order.model_dump()
        order = await self.order_repo.add(data=order_dict)
        return order

    async def get_orders(self):
        order = await self.order_repo.get_all_orders_with_related()
        return order

    async def get_order_by_id(self, order_id):
        order = await self.order_repo.get_order_with_related(order_id=order_id)
        return order

    async def approve_order_by_id(self, order_id: int):
        async with self.session.begin():
            order = await self.order_repo.get_order_with_related(order_id=order_id)
            user = order.user
            benefit = order.benefit

            if user.coins < benefit.price:
                return # TODO

            if order.status == Status.APPROVED:
                return # TODO
            
            user.coins -= benefit.price
            order.status = Status.APPROVED
            order.activated_at = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)

            if benefit.period is not None:
                order.ends_at = order.activated_at + PERIOD_MAP[benefit.period]
            
            self.session.add(user)
            self.session.add(order)
        
        return order

    async def reject_order_by_id(self, order_id: int):
        new_data = {'status': Status.REJECTED}
        rejected_order = await self.order_repo.update_by_id(id=order_id, new_data=new_data)
        return rejected_order

    async def update_order_by_id(self, order_id: int, new_data: OrderSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_order = await self.order_repo.update_by_id(id=order_id, new_data=new_data_dict)
        return updated_order

    async def delete_order_by_id(self, order_id: int):
        await self.order_repo.delete_by_id(id=order_id)
