from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.internal.repositories import OrderRepository
from app.internal.services import OrderService


class OrderFactory:
    @staticmethod
    def get_order_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
        return OrderService(OrderRepository, session)
