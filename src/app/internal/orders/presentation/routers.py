from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, status, UploadFile

from app.internal.access import get_current_user, is_admin, is_authorized
from app.internal.factories import CommentFactory, OrderFactory
from app.internal.services import CommentService, OrderService
from app.internal.schemas import (
    CommentSchemaRel,
    CommentSchemaAdd,
    OrderSchema,
    OrderSchemaAdd,
    OrderSchemaDetail,
    OrderSchemaUser,
    OrderSchemaBenefit,
    UserInfoSchema,
)


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.post('', dependencies=[Depends(is_authorized)])
async def add_order(
    order: OrderSchemaAdd,
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    new_order = await order_service.add_order(order=order, user_id=user_info.id)
    if new_order is not None:
        return new_order
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('', dependencies=[Depends(is_admin)])
async def get_orders(
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> list[OrderSchemaUser]:
    orders = await order_service.get_orders(user_id=user_info.id)
    return orders


@router.post('/{id}/approve', dependencies=[Depends(is_admin)])
async def approve_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    approved_order = await order_service.approve_order_by_id(order_id=id)
    return approved_order


@router.post('/{id}/reject', dependencies=[Depends(is_admin)])
async def reject_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    rejected_order = await order_service.reject_order_by_id(order_id=id)
    return rejected_order


@router.post('/{id}/cancel', dependencies=[Depends(is_authorized)])
async def cancel_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchema:
    cancelled_order = await order_service.cancel_order_by_id(order_id=id)
    return cancelled_order


@router.post('/{id}/comments', dependencies=[Depends(is_authorized)])
async def add_comment_by_order_id(
    id: int,
    message: Annotated[str, Form()],
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    comment_service: Annotated[CommentService, Depends(CommentFactory.get_comment_service)],
    attachment: Annotated[UploadFile | None, File()] = None,
) -> CommentSchemaRel:
    comment = CommentSchemaAdd(message=message)
    new_comment = await comment_service.add_comment(
        order_id=id,
        comment=comment,
        attachment=attachment,
        user_id=user_info.id
    )
    return new_comment


@router.get('/{id}', dependencies=[Depends(is_authorized)])
async def get_order_by_id(
    id: int,
    user_info: Annotated[UserInfoSchema, Depends(get_current_user)],
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
) -> OrderSchemaDetail:
    order = await order_service.get_order_by_id(order_id=id, user_id=user_info.id)
    return order


@router.delete('/{id}')
async def delete_order_by_id(
    id: int,
    order_service: Annotated[OrderService, Depends(OrderFactory.get_order_service)],
):
    await order_service.delete_order_by_id(order_id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
