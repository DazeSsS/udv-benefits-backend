import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_comments(client: AsyncClient, tokens_2, order_1, clear):
    access_token = (await tokens_2).access_token
    response = await client.get(
        f'/orders/{order_1.id}',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    order_empty = response.json()
    assert len(order_empty.get('comments')) == 0

    response = await client.post(
        f'/orders/{order_1.id}/comments',
        data={
            "message": 'Здравствуйте!'
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    new_comment = response.json()
    
    response = await client.get(
        f'/orders/{order_1.id}',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    order_with_comment = response.json()
    assert len(order_with_comment.get('comments')) == 1
