from zoneinfo import ZoneInfo
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.repositories import BenefitRepository, OrderRepository, UserRepository
from app.internal.orders.domain.schemas import OrderSchemaAdd, OrderSchemaUpdate
from app.internal.orders.db.models import Order, Status
from app.internal.benefits.db.models import PERIOD_MAP

from config import settings


class OrderService:
    def __init__(
        self,
        benefit_repo: BenefitRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.order_repo: OrderRepository = order_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.session = session

    async def add_order(self, order: OrderSchemaAdd):
        async with self.session.begin():
            benefit = await self.benefit_repo.get_by_id(id=order.benefit_id)
            user = await self.user_repo.get_by_id(id=order.user_id)

            if user.balance < benefit.price:
                return # TODO

            user.balance -= benefit.price

            order_dict = order.model_dump()
            order = Order(**order_dict)

            self.session.add(user)
            self.session.add(order)

        return order

    async def get_orders(self):
        order = await self.order_repo.get_all_orders_with_related()
        return order

    async def get_order_by_id(self, order_id):
        order = await self.order_repo.get_order_with_related(order_id=order_id)
        return order

    async def approve_order_by_id(self, order_id: int):
        order = await self.order_repo.get_order_with_related(order_id=order_id)
        benefit = order.benefit

        if order.status == Status.APPROVED:
            return # TODO

        status = Status.APPROVED
        activated_at = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)

        new_data = {
            'status': status,
            'activated_at': activated_at
        }

        if benefit.period is not None:
            new_data.update(
                {'ends_at': activated_at + PERIOD_MAP[benefit.period]}
            )

        updated_order = await self.order_repo.update_by_id(id=order_id, new_data=new_data)
        return updated_order

    async def reject_order_by_id(self, order_id: int):
        async with self.session.begin():
            rejected_order = await self.order_repo.get_order_with_related(order_id=order_id)

            if rejected_order.status == Status.REJECTED:
                return # TODO

            user = rejected_order.user
            benefit = rejected_order.benefit

            user.balance += benefit.price

            rejected_order.status = Status.REJECTED
            rejected_order.activated_at = None
            rejected_order.ends_at = None

            self.session.add(user)
            self.session.add(rejected_order)

        return rejected_order

    async def update_order_by_id(self, order_id: int, new_data: OrderSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_order = await self.order_repo.update_by_id(id=order_id, new_data=new_data_dict)
        return updated_order

    async def delete_order_by_id(self, order_id: int):
        await self.order_repo.delete_by_id(id=order_id)
