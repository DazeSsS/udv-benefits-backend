import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_1, tokens_1, clear):
    response = await client.post(
        '/users',
        json={
            "email": "example2@gmail.com",
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "birth_date": "2004-04-29",
            "phone": "89573456195",
            "has_children": "true",
            "work_start_date": "2023-09-18",
            "legal_entity": "UDV",
            "position": "backend",
            "department": "Backend"
        }
    )
    user = response.json()
    del user['createdAt']
    assert {
        'email': 'example2@gmail.com',
        'firstName': 'Иван',
        'lastName': 'Иванов',
        'middleName': 'Иванович',
        'birthDate': '2004-04-29',
        'phone': '89573456195',
        'hasChildren': True,
        'isAdmin': False,
        'isVerified': False,
        'workStartDate': '2023-09-18',
        'workEndDate': None,
        'legalEntity': 'UDV',
        'position': 'backend',
        'department': 'Backend',
        'id': 2,
        'profilePhoto': None,
        'balance': 2000,
        'workExperience': {
            'years': 1,
            'months': 2
        },
        'age': 20
    } == user


@pytest.mark.asyncio
async def test_verify_user(client: AsyncClient, user_1, user_2, tokens_1, clear):
    assert user_2.is_verified == False
    response = await client.patch(
        f'/users/{user_2.id}/verify',
        json={}
    )
    verified_user = response.json()
    assert verified_user.get('isVerified') == True

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, user_1, tokens_1, clear):
    response = await client.get(
        '/users/me',
        headers={
            'Authorization': f'Bearer {(await tokens_1).access_token}'
        }
    )
    user = response.json()
    del user['createdAt']
    assert {
        "id": 1,
        "email": "example@gmail.com",
        "firstName": "Иван",
        "lastName": "Иванов",
        "middleName": "Иванович",
        "birthDate": "2004-04-29",
        "phone": "89573456195",
        "profilePhoto": None,
        "hasChildren": True,
        "isAdmin": True,
        "isVerified": True,
        "workStartDate": "2024-09-18",
        "workEndDate": None,
        "legalEntity": "UDV",
        "position": "hr",
        "department": "HR",
        "balance": 2000,
        'workExperience': {
            'years': 0,
            'months': 2
        },
        'age': 20
    } == user

@pytest.mark.asyncio
async def test_get_user_orders(client: AsyncClient, user_2, tokens_2, order_1, clear):
    response = await client.get(
        '/users/me/orders',
        headers={
            'Authorization': f'Bearer {(await tokens_2).access_token}'
        }
    )
    orders = response.json()
    del orders[0]['createdAt']
    del orders[0].get('benefit')['createdAt']
    assert [
        {
            'benefitId': 1,
            'optionId': 1,
            'id': 1,
            'status': 'in_work',
            'userId': 1,
            'activatedAt': None,
            'endsAt': None,
            'benefit': {
                'id': 1,
                'title': 'Скидка на ДМС от "Альфа-Страхование"',
                'provider': 'Альфа-Страхование',
                'description': 'Выбирайте оптимальный уровень медицинского страхования в зависимости от ваших нужд. ДМС от "Альфа-Страхование" предлагает три уровня покрытия, от базового до премиального, чтобы каждый нашел вариант для себя.',
                'picture': 'https://storage.yandexcloud.net/udv-benefits-bucket/benefits/default/health/%D0%94%D0%9C%D0%A1_%D0%BE%D0%B1%D1%89%D0%B8%D0%B9.jpg',
                'price': 1000,
                'requiredExperience': None,
                'childsRequired': False,
                'categoryId': 1,
                'isActive': True,
                'category': {
                    'title': 'Здоровье',
                    'id': 1,
                    'icon': None
                }
            },
            'unreadComments': 0
        }
    ] == orders
