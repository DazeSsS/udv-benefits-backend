from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.internal.dependencies import order_service
from app.internal.orders.domain.schemas import OrderSchema, OrderSchemaAdd
from app.internal.orders.domain.services import OrderService


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.post('')
async def add_order(
    order: OrderSchemaAdd,
    order_service: Annotated[OrderService, Depends(order_service)],
) -> OrderSchema:
    new_order = await order_service.add_order(order=order)
    return new_order


@router.get('')
async def get_orders(
    ascending: bool,
    order_service: Annotated[OrderService, Depends(order_service)],
) -> list[OrderSchema]:
    orders = await order_service.get_orders(ascending=ascending)
    return orders


@router.post('/{id}/approve')
async def approve_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(order_service)],
) -> OrderSchema:
    approved_order = await order_service.approve_order_by_id(order_id=id)
    return approved_order


@router.post('/{id}/reject')
async def reject_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(order_service)],
) -> OrderSchema:
    rejected_order = await order_service.reject_order_by_id(order_id=id)
    return rejected_order


@router.get('/{id}')
async def get_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(order_service)],
) -> OrderSchema:
    order = await order_service.get_order_by_id(order_id=id)
    return order


@router.delete('/{id}')
async def delete_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(order_service)],
):
    await order_service.delete_order_by_id(order_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
