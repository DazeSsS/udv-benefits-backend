from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.internal.access import get_current_user
from app.internal.factories import OrderFactory
from app.internal.services import OrderService
from app.internal.orders.domain.schemas import OrderSchema, OrderSchemaAdd, OrderSchemaAllRel, OrderSchemaBenefits
from app.internal.users.domain.schemas import UserInfoSchema


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.post('')
async def add_order(
    order: OrderSchemaAdd,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    new_order = await order_service.add_order(order=order)
    if new_order is not None:
        return new_order
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('')
async def get_orders(
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> list[OrderSchemaAllRel]:
    orders = await order_service.get_orders()
    return orders


@router.post('/{id}/approve')
async def approve_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    approved_order = await order_service.approve_order_by_id(order_id=id)
    return approved_order


@router.post('/{id}/reject')
async def reject_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    rejected_order = await order_service.reject_order_by_id(order_id=id)
    return rejected_order


@router.get('/{id}')
async def get_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchemaAllRel:
    order = await order_service.get_order_by_id(order_id=id)
    return order


@router.delete('/{id}')
async def delete_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
):
    await order_service.delete_order_by_id(order_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
