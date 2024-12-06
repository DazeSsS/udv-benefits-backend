import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, user_2, tokens_2, benefit_1, clear):
    response = await client.post(
        '/orders',
        json={
            "benefitId": benefit_1.id,
            "optionId": 1
        },
        headers={
            'Authorization': f'Bearer {(await tokens_2).access_token}'
        }
    )
    order = response.json()
    del order['createdAt']
    assert {
        'benefitId': benefit_1.id,
        'optionId': 1,
        'id': 1,
        'status': 'in_work',
        'userId': user_2.id,
        'activatedAt': None,
        'endsAt': None
    } == order

@pytest.mark.asyncio
async def test_approve_order(client: AsyncClient, user_1, user_2, tokens_1, benefit_1, order_1, clear):
    assert order_1.status == 'in_work'
    response = await client.post(
        f'/orders/{order_1.id}/approve',
        headers={
            'Authorization': f'Bearer {(await tokens_1).access_token}'
        }
    )
    approved_order = response.json()
    assert approved_order.get('status') == 'approved'

@pytest.mark.asyncio
async def test_approve_order(client: AsyncClient, tokens_1, order_1, clear):
    assert order_1.status == 'in_work'
    response = await client.post(
        f'/orders/{order_1.id}/approve',
        headers={
            'Authorization': f'Bearer {(await tokens_1).access_token}'
        }
    )
    approved_order = response.json()
    assert approved_order.get('status') == 'approved'

@pytest.mark.asyncio
async def test_reject_order(client: AsyncClient, tokens_1, order_1, clear):
    assert order_1.status == 'in_work'
    response = await client.post(
        f'/orders/{order_1.id}/reject',
        headers={
            'Authorization': f'Bearer {(await tokens_1).access_token}'
        }
    )
    approved_order = response.json()
    assert approved_order.get('status') == 'rejected'
