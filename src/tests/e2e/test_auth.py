import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth(client: AsyncClient, user_1, login_token_1, clear):
    response = await client.post(
        '/auth/token/login',
        params={'token': login_token_1}
    )
    tokens = response.json()

    assert 'accessToken' in tokens
    assert 'refreshToken' in tokens

    await asyncio.sleep(1)

    response = await client.post(
        '/auth/token/refresh',
        params={'refresh_token': tokens.get('refreshToken')}
    )
    refreshed_tokens = response.json()

    assert 'accessToken' in refreshed_tokens
    assert 'refreshToken' in refreshed_tokens
