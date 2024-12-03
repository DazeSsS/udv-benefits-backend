from zoneinfo import ZoneInfo
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.models import Order
from app.internal.schemas import OrderSchemaAdd, OrderSchemaUpdate, OrderSchemaUser, PERIOD_MAP, Status, UserInfoSchema
from app.internal.repositories import BenefitRepository, CommentRepository, OrderRepository, UserRepository

from config import settings


class OrderService:
    def __init__(
        self,
        benefit_repo: BenefitRepository,
        comment_repo: CommentRepository,
        order_repo: OrderRepository,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.comment_repo: CommentRepository = comment_repo(session)
        self.order_repo: OrderRepository = order_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.session = session

    async def add_order(self, order: OrderSchemaAdd, user_id: int):
        async with self.session.begin():
            benefit = await self.benefit_repo.get_by_id(id=order.benefit_id)
            user = await self.user_repo.get_by_id(id=user_id)

            if user.balance < benefit.price:
                return # TODO

            user.balance -= benefit.price

            order_dict = order.model_dump()
            order_obj = Order(user_id=user_id, **order_dict)

            self.session.add(user)
            self.session.add(order_obj)

        return order_obj

    async def get_orders(self, user_id: int):
        orders = await self.order_repo.get_all_orders_with_related()

        result_orders = []
        for order in orders:
            comments_count = await self.comment_repo.get_unread_comments_count(
                order_id=order.id, user_id=user_id
            )

            order_user = OrderSchemaUser.model_validate(order)
            order_user.unread_comments = comments_count

            result_orders.append(order_user)

        return result_orders

    async def get_order_by_id(self, order_id: int, user_id: int):
        order = await self.order_repo.get_order_with_related(order_id=order_id)
        comments = order.comments

        if comments:
            unread_comments = [
                comment for comment in comments
                if not comment.is_read
                and comment.sender_id != user_id
            ]
            for comment in unread_comments:
                comment.is_read = True

            if unread_comments:
                await self.comment_repo.session.commit()

        return order

    async def approve_order_by_id(self, order_id: int):
        order = await self.order_repo.get_order_with_benefit(order_id=order_id)
        benefit = order.benefit

        if order.status == Status.APPROVED:
            return # TODO

        status = Status.APPROVED
        activated_at = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)

        new_data = {
            'status': status,
            'activated_at': activated_at
        }

        if benefit.content.period is not None:
            new_data.update(
                {'ends_at': activated_at + PERIOD_MAP[benefit.content.period]}
            )

        updated_order = await self.order_repo.update_by_id(id=order_id, new_data=new_data)
        return updated_order

    async def reject_order_by_id(self, order_id: int):
        async with self.session.begin():
            rejected_order = await self.order_repo.get_order_with_benefit(order_id=order_id)

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
